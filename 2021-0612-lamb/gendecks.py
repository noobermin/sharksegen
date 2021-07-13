#!/usr/bin/env python
'''
./gendeck.py
'''
from pys import savetxt,sd, destr;
import re;
from copy import deepcopy;
import numpy as np;
tmplname = 'tmpl.deck';
with open(tmplname,'r') as f:
    tmpl = f.readlines();

subs = {
    'I0'  : 1e19,
    'lam' : (0.8,'micron'),
    't0'  : (80,'femto')};

def genopt(v):
    u = ''
    if type(v) is tuple:
        u = '*'+v[1];
        v=v[0];
    f,w = np.modf(v);
    if w > 100:
        vs = f'{v:e}' 
    elif np.isclose(f,0.0):
        vs = f'{int(v):d}'
    else:
        vs = f'{v:f}';
    return vs + u;

def sub_opt(tmpl, label, sub):
    def subl(l, label, sub):
        m = re.match(f'( *{label} *= ).+$', l);
        if m:
            return m.group(1) + genopt(sub) + '\n';
        return l;
    tmpl[:] = [ subl(l,label,sub) for l in tmpl ];

def gendeck(tmpl, subs):
    cur = deepcopy(tmpl);
    for l, sub in subs.items():
        sub_opt(tmpl, l, sub)
    return ''.join(tmpl);

Is = [1e19, 1e20, 1e21];
ls = [0.8,  0.26]
ts = [80];
ds = [ sd(subs, I0=I0, lam=(lam, 'micron'), t0=(t0,'femto'))
       for I0  in Is
       for lam in ls
       for t0  in ts ]
N=0
for d in ds:
    I0, (lam,_), (t0,_) = destr(d, 'I0', 'lam', 't0');
    name = f'wat2d{N:02}_lam={lam:.2f}_I={I0:0.0e}_t0={t0:05.1f}.deck'
    print(f">>>{name}");
    savetxt(name, gendeck(tmpl, d));
    
    
