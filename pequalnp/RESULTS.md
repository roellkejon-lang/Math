# pequalnp.com steps worked on (2026-11-26, GitHub handle roellkejon-lang)

Every step below was **false as posted**. Each one asked for a circuit smaller than the true
minimum. Each was handed back to the desk with reason `statement_seems_false`. No points were
earned, since the desk credits only accepted proofs.

| Step | Function | Asked | True minimum | Evidence |
|---|---|---|---|---|
| L-meta-20477 | 3×5 graph, mask 1226, monotone AND/OR, one-a-side promise | ≤ 6 | 7 | exhaustive search (`L-meta-20477/search.c`), SAT (`tools/find_rep.py`), hand proof, and a **Lean proof of the negation** (`L-meta-20477/NotRepSize6.lean`) |
| L-meta-23069 | 3×6 graph, mask 5054, monotone AND/OR, one-a-side promise | ≤ 8 | 9 (the desk holds 9) | SAT: `find_rep.py 3 6 5054 8` is UNSAT (about 10 min) |
| L-meta-24781 | two-lit function of a 6-point graph, mask 2113687, AND/OR/NOT fan-in two | ≤ 9 | 10 (the desk holds 10) | SAT: `find_twolit.py 6 2113687 9` is UNSAT (about 36 min). At 10 it finds a circuit in seconds |

## The SAT encoders (`tools/`)

Each gate has one-hot selectors for its two inputs, chosen from earlier wires. Its operation
is AND or OR, plus NOT in `find_twolit.py`, where NOT reads its first input. There is one
value variable per gate per promised input. The output is the last gate, which loses nothing,
because a smaller circuit pads with a copy gate. Constant gates, single-input copies and reads
of missing wires never save a gate, so leaving them out keeps "UNSAT" a true lower bound under
the project's `Circuit` model. Every circuit found is checked again in Python. As a check,
`find_rep.py 3 5 1226 6` is UNSAT and `… 7` finds a circuit, which agrees with the exhaustive
search.

```
find_rep.py    n m MASK s CADICAL     # graph A u v = MASK.testBit (m*u + v)
find_twolit.py N MASK s CADICAL       # f(i,j) = MASK.testBit (N*min(i,j) + max(i,j)), i = j allowed
```

`CADICAL` is the binary shipped with the Lean toolchain (`~/.elan/toolchains/*/bin/cadical`).

Only L-meta-20477 has a Lean proof of the negation. The other two lower bounds rest on the
SAT runs alone, with no LRAT certificate or Lean file yet.
