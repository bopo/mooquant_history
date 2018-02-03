# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

from .standard import IF, REF

__all__ = ('NJJ', 'NHJ', 'DFP')

# def NJJ(df, n):
#     '''新将军策略'''
#     D0=n;
#     D1=D0+1;
#     D2=D1+1;
#     D3=D2+1;
#     D4=D3+1;

#     ((REF(V,D0) < REF(V,D3)).values == (REF(V,D1) < REF(V,D3)).values == (REF(V,D2) < REF(V,D3))).values ==
#     ((REF(C,D0) > REF(O,D3)).values == (REF(C,D1) > REF(O,D3)).values == (REF(C,D2) > REF(O,D3))).values ==
#     (REF(C,D3) > REF(O,D3)).values == REF(O,D0) > 0.values == REF(V,D0) > 0.values == 
#     ((REF(L,D0) > REF(L,D3)).values == (REF(L,D1) > REF(L,D3)).values == (REF(L,D2) > REF(L,D3))).values ==
#     ((REF(H,D3) - REF(L,D3)) / REF(L, D3) >= 0.04).values;

# def NHJ(df, n):
#     '''新黄金策略'''
#     pass

# def DFP(df, n=0):
#     '''多方炮策略'''
#     D0 = n;
#     D1 = D0+1;
#     D2 = D1+1;
#     D3 = D2+1;

#     C = df.close
#     O = df.open
#     V = df.volume

#     M1 = ((REF(C, D2) - REF(C, D3)) / REF(C, D3) >= 0.03).values
#     M2 = M1 == (REF(C, D1) < REF(O, D1)).values
#     M3 = M2 == (REF(C, D1) > REF(O, D2)).values
#     M4 = M3 == (REF(V, D1) < REF(V, D2)).values
#     M5 = M4 == (REF(C, D1) < REF(O, D1)).values
#     M6 = M5 == (REF(C, D0) > REF(O, D1)).values

#     df['DFP'] = M6
    
#     return df['DFP']


