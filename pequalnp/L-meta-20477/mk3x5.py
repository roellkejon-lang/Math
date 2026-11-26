import re, sys
src, out, ns, M = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
n, m = 3, 5
A = lambda u, v: (M >> (m * u + v)) & 1 == 1
pos = [(u, v) for u in range(n) for v in range(m) if A(u, v)]
neg = [(u, v) for u in range(n) for v in range(m) if not A(u, v)]
P, Q = len(pos), len(neg); N = P * Q
def samp(k): return neg[k % Q] if k < N else pos[(k - N) // Q]
def onehot(u, v): return [i == u for i in range(n)] + [j == v for j in range(m)]
raw = []
for w in range(n + m):
    x = 0
    for k in range(2 * N):
        if onehot(*samp(k))[w]: x |= 1 << k
    raw.append(x)
t = open(src, encoding='utf-8').read()
# keep only the lower-bound part: drop the upper bound and the final conjunction
t = t[:t.index('def upperC : Circuit :=')] + 'end PEqualNP.Outside.L_meta_5469\n'
t = re.sub(r'\b120\b', str(2 * N), t); t = re.sub(r'\b60\b', str(N), t)
t = t.replace('% 6)', f'% {Q})').replace('/ 6)', f'/ {Q})')
t = t.replace('L_meta_5469', ns)
t = re.sub(r'def rawInputs : List W :=\n  \[[^\]]*\]', 'def rawInputs : List W :=\n  [' + ', '.join(hex(x) for x in raw) + ']', t)
t = re.sub(r'def A : Fin 4 → Fin 4 → Bool := fun u v : Fin 4 => \(1983 : ℕ\)\.testBit \(4 \* u\.val \+ v\.val\)',
           f'def A : Fin {n} → Fin {m} → Bool := fun (u : Fin {n}) (v : Fin {m}) => ({M} : ℕ).testBit ({m} * u.val + v.val)', t)
L = lambda xs: '[' + ', '.join(f'({u}, {v})' for u, v in xs) + ']'
t = re.sub(r'def posL : List \(Fin 4 × Fin 4\) :=\n  \[[^\]]*\]', f'def posL : List (Fin {n} × Fin {m}) :=\n  {L(pos)}', t)
t = re.sub(r'def negL : List \(Fin 4 × Fin 4\) :=\n  \[[^\]]*\]', f'def negL : List (Fin {n} × Fin {m}) :=\n  {L(neg)}', t)
t = t.replace('def samp (k : Fin %d) : Fin 4 × Fin 4 :=' % (2 * N), 'def samp (k : Fin %d) : Fin %d × Fin %d :=' % (2 * N, n, m))
assert 'Fin 4' not in t, [l for l in t.splitlines() if 'Fin 4' in l]
t += (f'\ntheorem PEqualNP.Outside.{ns} : ¬ PEqualNP.Represents.RepSizeAtMost '
      f'(fun (u : Fin {n}) (v : Fin {m}) => ({M} : ℕ).testBit ({m} * u.val + v.val)) 6 := by\n'
      f'  rintro ⟨C, hm, hs, hr⟩\n  exact PEqualNP.Outside.{ns}.no_small C hm hs hr\n')
open(out, 'w', encoding='utf-8', newline='\n').write(t)
print('pos', pos, 'neg', neg, 'N', N)
