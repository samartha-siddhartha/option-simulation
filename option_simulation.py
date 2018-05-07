# -*- coding: utf-8 -*-
"""
Created on Mon May  7 08:48:39 2018

@author: SamarthaS
"""

import mibian
import pandas as pd
import numpy as np


    
def createrange(strike, vol, udif):
    strike = int(strike)
    udif = int(udif)
    vol  = float(vol)    
    uprice_list = []
    vol_list = []
    vol_list.append(vol)
    uprice_list.append(strike)
    uvol = float(vol)
    dvol = float(vol)
    uprice = strike
    dprice = strike
    udif =int(udif)
    for val in range(3):
        u = uvol + 1
        n = dvol - 1
        m = uprice + udif
        v = dprice - udif
        uprice_list.append(m)
        uprice_list.append(v)
        vol_list.append(u)
        vol_list.append(n)
        uvol = u
        dvol = n
        uprice = m
        dprice = v
    uprice_list = sorted(uprice_list)
    vol_list = sorted(vol_list)
    return[uprice_list,vol_list]
            
              
def call_table(undprice,strike,days,vol,udif,greek):
    interest_rate =6
    call =[]
    f = createrange(strike,vol,udif)
    for iv in f[1]:
        m =[]
        m.append(iv)
        for stk in f[0]:
            factor =mibian.BS([undprice,stk,interest_rate,days],volatility=iv)
            if greek =='Option Price':
                m.append(round(factor.callPrice,2))
            elif greek =='Delta':
                m.append(round(factor.callDelta,2))
            elif greek =='Gamma':
                m.append(round(factor.gamma,4))
            elif greek=='Theta':
                m.append(round(factor.callTheta,2))
            else:
                m.append(round(factor.vega,4))
        call.append(m)
    call =pd.DataFrame(call,columns=['IV']+['Strike '+str(i) for i in f[0]])
    return call


def put_table(undprice,strike,days,vol,udif,greek):
    interest_rate =6
    call =[]
    f = createrange(strike,vol,udif)
    for iv in f[1]:
        m =[]
        m.append(iv)
        for stk in f[0]:
            factor =mibian.BS([undprice,stk,interest_rate,days],volatility=iv)
            if greek =='Option Price':
                m.append(round(factor.putPrice,2))
            elif greek =='Delta':
                m.append(round(factor.putDelta,2))
            elif greek =='Gamma':
                m.append(round(factor.gamma,4))
            elif greek=='Theta':
                m.append(round(factor.putTheta,2))
            else:
                m.append(round(factor.vega,4))
        call.append(m)
    put= pd.DataFrame(call,index =f[1],columns=['IV']+['Strike '+str(i) for i in f[0]])
    return put
    