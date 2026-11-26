# Find an AND/OR/NOT fan-in-2 circuit with s gates for the two-lit function of a 6-point graph.
import sys, subprocess, itertools
N, M, s = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); cad = sys.argv[4]
rows = []
for i in range(N):
    for j in range(i, N):
        x = [k in (i, j) for k in range(N)]
        rows.append((x, (M >> (N * min(i, j) + max(i, j))) & 1 == 1))
I = N; nv = 0; C = []
def new():
    global nv; nv += 1; return nv
sel = {}; isor = {}; isnot = {}; val = {}
for j in range(s):
    W = I + j
    for side in (0, 1):
        vs = [new() for _ in range(W)]; sel[j, side] = vs
        C.append(vs[:])
        for a, b in itertools.combinations(vs, 2): C.append([-a, -b])
    isor[j] = new(); isnot[j] = new(); C.append([-isor[j], -isnot[j]])
    for r in range(len(rows)): val[I + j, r] = new()
def wv(w, r): return rows[r][0][w] if w < I else val[w, r]
for j in range(s):
    for r in range(len(rows)):
        z = val[I + j, r]; t = []
        for side in (0, 1):
            tv = new(); t.append(tv)
            for w, sv in enumerate(sel[j, side]):
                x = wv(w, r)
                if x is True: C.append([-sv, tv])
                elif x is False: C.append([-sv, -tv])
                else: C += [[-sv, -x, tv], [-sv, x, -tv]]
        a, b = t; o, nt = isor[j], isnot[j]
        C += [[-o, -a, z], [-o, -b, z], [-o, -z, a, b]]                    # OR
        C += [[-nt, a, z], [-nt, -a, -z]]                                    # NOT a
        C += [[o, nt, -z, a], [o, nt, -z, b], [o, nt, z, -a, -b]]            # AND
for r, (x, y) in enumerate(rows): C.append([val[I + s - 1, r] if y else -val[I + s - 1, r]])
cnf = f'p cnf {nv} {len(C)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in C)
res = subprocess.run([cad, '-q'], input=cnf, capture_output=True, text=True)
if res.returncode == 20: print(f'UNSAT: no circuit with {s} gates'); sys.exit(0)
assert res.returncode == 10, res.returncode
T = {int(v) for line in res.stdout.splitlines() if line.startswith('v') for v in line.split()[1:] if int(v) > 0}
gates = []
for j in range(s):
    a, b = [next(w for w, sv in enumerate(sel[j, side]) if sv in T) for side in (0, 1)]
    o = 'or' if isor[j] in T else 'not' if isnot[j] in T else 'and'
    gates.append((o, [a] if o == 'not' else [a, b]))
for x, y in rows:
    w = list(x)
    for o, ins in gates:
        w.append(not w[ins[0]] if o == 'not' else any(w[k] for k in ins) if o == 'or' else all(w[k] for k in ins))
    assert w[-1] == y
print(f'FOUND {s} gates, output wire {I + s - 1}:', gates)
