# Find a monotone fan-in-2 circuit with s gates representing an n x m graph (one-a-side promise).
import sys, subprocess, itertools
n, m, M, s = map(int, sys.argv[1:5]); cad = sys.argv[5]
A = lambda u, v: (M >> (m * u + v)) & 1 == 1
I = n + m; rows = [(u, v) for u in range(n) for v in range(m)]
nv = 0; C = []
def new():
    global nv; nv += 1; return nv
def inval(w, r):  # input wire value on row r
    u, v = rows[r]; return (w == u) if w < n else (w - n == v)
sel = {}; op = {}; val = {}
for j in range(s):
    W = I + j
    for side in (0, 1):
        vs = [new() for _ in range(W)]; sel[j, side] = vs
        C.append(vs[:])
        for a, b in itertools.combinations(vs, 2): C.append([-a, -b])
    op[j] = new()  # true = OR, false = AND
    for r in range(len(rows)): val[I + j, r] = new()
def wv(w, r):  # literal or bool
    return inval(w, r) if w < I else val[w, r]
for j in range(s):
    g = I + j
    for r in range(len(rows)):
        z = val[g, r]
        # t_side = value of selected input on side
        t = []
        for side in (0, 1):
            tv = new(); t.append(tv)
            for w, sv in enumerate(sel[j, side]):
                x = wv(w, r)
                if x is True: C.append([-sv, tv])
                elif x is False: C.append([-sv, -tv])
                else: C += [[-sv, -x, tv], [-sv, x, -tv]]
        a, b = t; o = op[j]
        # OR: z <-> a|b ; AND: z <-> a&b
        C += [[-o, -a, z], [-o, -b, z], [-o, -z, a, b]]
        C += [[o, -z, a], [o, -z, b], [o, z, -a, -b]]
# output = last gate
for r, (u, v) in enumerate(rows):
    C.append([val[I + s - 1, r]] if A(u, v) else [-val[I + s - 1, r]])
cnf = f'p cnf {nv} {len(C)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in C)
res = subprocess.run([cad, '-q'], input=cnf, capture_output=True, text=True)
if res.returncode == 20: print(f'UNSAT: no circuit with {s} gates'); sys.exit(0)
assert res.returncode == 10, res.returncode
true = {int(x) for line in res.stdout.splitlines() if line.startswith('v') for x in line.split()[1:] if int(x) > 0}
gates = []
for j in range(s):
    ins = [next(w for w, sv in enumerate(sel[j, side]) if sv in true) for side in (0, 1)]
    gates.append(('or' if op[j] in true else 'and', ins))
# verify independently
def ev(u, v):
    w = [inval(k, rows.index((u, v))) for k in range(I)]
    for o, (a, b) in gates: w.append((w[a] or w[b]) if o == 'or' else (w[a] and w[b]))
    return w[-1]
assert all(ev(u, v) == A(u, v) for u, v in rows)
print(f'FOUND {s} gates, output wire {I + s - 1}:')
for j, (o, ins) in enumerate(gates): print(f'  w{I + j} = {o.upper()}(w{ins[0]}, w{ins[1]})')
