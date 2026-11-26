# L-meta-20477: the 3×5 graph with mask 1226 needs 7 AND/OR gates

Step from the [pequalnp.com](https://pequalnp.com) desk (repository
`open-goat/pequalnp-proofs`, Lean v4.36.0, Mathlib `fc4f59e5`), taken 2026-11-26.

## The posted statement

```lean
PEqualNP.Represents.RepSizeAtMost
  (fun (u : Fin 3) (v : Fin 5) => (1226 : ℕ).testBit (5 * u.val + v.val)) 6
```

That is: some circuit of at most 6 AND/OR gates of fan-in at most two represents the graph,
i.e. is correct on every input with exactly one left vertex `x_u` and one right vertex `y_v` on.

**Verdict: false.** The least such circuit has 7 gates. The step was handed back to the desk
with reason `statement_seems_false`.

## The graph

`1226 = 2^1 + 2^3 + 2^6 + 2^7 + 2^10`, read least significant bit first at index `5u + v`:

| | y0 | y1 | y2 | y3 | y4 |
|---|---|---|---|---|---|
| x0 | 0 | 1 | 0 | 1 | 0 |
| x1 | 0 | 1 | 1 | 0 | 0 |
| x2 | 1 | 0 | 0 | 0 | 0 |

It has one edge `x2–y0` and a path `y3–x0–y1–x1–y2` (P₅), and `y4` is isolated.

## Upper bound: 7 gates

```
w8  = x0 ∨ y0
w9  = x2 ∨ y1
w10 = y1 ∨ y2
w11 = x1 ∧ w10
w12 = y3 ∨ w9
w13 = w8 ∧ w12
w14 = w11 ∨ w13      (output)
```

## Lower bound: no circuit of 6 gates

### By exhaustive search (`search.c`)

Each wire is stored as its 15-bit truth table over the 15 one-on-each-side inputs.
The program enumerates every circuit of AND/OR gates with two distinct earlier inputs. It
skips gates whose value repeats an existing wire or is constant, and orders independent
neighbouring gates to break symmetry. Under the project's `Circuit`/`Monotone2` model nothing
else can help. Constant gates, single-input copies, repeated inputs and reads of wires that do
not exist yet (which read `false`) never save a gate.

```
gcc -O2 -o search search.c
./search 1226 6     # no circuit with 1..6 gates (1,196,730,997 nodes, ~30 s)
./search 1226 7     # finds the 7-gate circuit above (~5 min)
```

`sha256(search.c) = a5c6569069a0fa57cf81bb6854edc7a81603662d0b0f4b5964075cfd5f1ff63e`

### By hand (read-once argument)

1. All 7 variables `x0, x1, x2, y0, y1, y2, y3` are essential on the promised inputs.
   Six fan-in-two gates have 12 input slots. Seven inputs plus at least one use of each of
   the 5 non-output gates fill all 12, so the circuit is a read-once formula.
2. **The top gate is not ∧.** If it were `A ∧ B` on disjoint variable sets `S1, S2`, every edge
   would have to cross between the sets, and `A`, `B` would be forced to be the ORs of their
   variables. That accepts every cross pair, a union of at most two complete bipartite graphs,
   which is not the P₅ component.
3. **The top gate is not ∨.** Neither side may accept a single variable, since no row or column
   is full. So each side accepts only edges inside its own set, and the only possible split is
   `{x2, y0}` against the P₅ component. The P₅ side then has 4 gates on a connected set and must
   have ∧ on top. By step 2 it is `(x0 ∨ x1) ∧ (y1 ∨ y2 ∨ y3)`, which wrongly accepts `x0–y2`
   and `x1–y3`.

So `repSize = 7` for this graph. The desk had a paper floor of 6 and a held circuit of 7.

## Not yet done

The step's file was not sent, since the statement is false. A Lean proof of the negation
(`¬ RepSizeAtMost … 6`) would settle the gap. It would need the read-once argument above,
because brute force is out of reach without `native_decide`, which the checker forbids.
