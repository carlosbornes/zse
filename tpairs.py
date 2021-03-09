__all__ = ['get_pairs']

from zse.rings import *
from zse.utilities import *
from zse.collections import *
from zse.ring_utilities import *
from zse.substitute import *

import numpy as np
import math

def get_pairs(code,validation='d2'):
    tr,lr,traj = get_fwrings(code,validation=validation)
    z = framework(code)
    ring_sizes = get_ring_sizes(code)
    max_ring = max(ring_sizes)*2
    traj = []
    alltlist = []
    allpairlist=[]
    ring_list = []
    for r in sorted(tr):
        for nn in range(2,math.floor(r/2)+1):
            for q,trs in enumerate(tr[r]):
                tlist = []
                pair_list = []
                tp = trs + trs
                lp = lr[r][q] + lr[r][q]
                z = framework(code)
                repeat = atoms_to_graph(z,tp[0],max_ring)[2]
                z2 = z.repeat(repeat)
                for i in range(1,len(trs)-nn,2):

                    pair_inner = lp[i-1:i+2*nn+2]
                    pair_id = '_'.join(pair_inner)
                    pair_inner.reverse()
                    r_pair_id = '_'.join(pair_inner)

                    t1label = [lp[i-1],lp[i],lp[i+1]]
                    t2label = [lp[i+2*nn-1],lp[i+2*nn],lp[i+2*nn+1]]

                    tinds = [tp[i],tp[i+2*nn]]

                    flag = False
                    if pair_id in pair_list or r_pair_id in pair_list:
                        flag = True


                    if not flag:
                        zl = len(z2)
                        ozl = len(z)
                        indices = np.arange(zl)
                        indices = indices.reshape(np.prod(repeat),ozl)
                        newinds = []
                        for ti in tinds:
                            newinds.append(int(np.where(indices==ti)[1]))
                        z3=z.copy()
                        z3 = tsub(z3,newinds,'Al')
                        traj +=[z3]
                        pair_list.append(pair_id)
                        alltlist.append(tinds)
                        allpairlist.append([t1label,t2label])
                        ring_list.append('{0}-MR {1}NN'.format(r,nn))
                        if nn==r/2:
                            pair_inner = lp[i+2*nn-1:2*(i+2*nn)+1]
                            pair_id = '_'.join(pair_inner)
                            pair_inner.reverse()
                            r_pair_id = '_'.join(pair_inner)
                            pair_list.append(pair_id)
    pairs = []
    for r,c in zip(ring_list,allpairlist):
        pairs.append('{0} | {1}'.format(r,c))

    return pairs,traj
