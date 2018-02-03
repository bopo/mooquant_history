# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd


def EMA(DF, N=5):
    return pd.Series.ewm(DF, span=N, min_periods=N - 1, adjust=True).mean()


def MA(DF, N=5):
    return pd.Series.rolling(DF, N).mean()


def SMA(DF, N, M):
    DF = DF.fillna(0)
    z = len(DF)
    var = np.zeros(z)
    var[0] = DF[0]

    for i in range(1, z):
        var[i] = (DF[i] * M + var[i - 1] * (N - M)) / N

    for i in range(z):
        DF[i] = var[i]

    return DF


def ATR(DF, N):
    C = DF['Close']
    H = DF['High']
    L = DF['Low']
    
    TR1 = MAX(MAX((H - L), ABS(REF(C, 1) - H)), ABS(REF(C, 1) - L))
    atr = MA(TR1, N)

    return atr


def HHV(DF, N):
    return pd.Series.rolling(DF, N).max()


def LLV(DF, N):
    return pd.Series.rolling(DF, N).min()


def SUM(DF, N):
    return pd.Series.rolling(DF, N).sum()


def ABS(DF):
    return DF.abs()


def MAX(A, B):
    var = IF(A > B, A, B)
    return var


def MIN(A, B):
    var = IF(A < B, A, B)
    return var


def IF(COND, V1, V2):
    var = np.where(COND, V1, V2)

    for i in range(len(var)):
        V1[i] = var[i]

    return V1IF


def REF(DF, N):
    VAR = DF.diff(N)
    VAR = DF - VAR
    return VAR


def STD(DF, N):
    return pd.Series.rolling(DF, N).std()


def MACD(DF, FAST, SLOW, MID):
    EMAFAST = EMA(DF, FAST)
    EMASLOW = EMA(DF, SLOW)

    DIFF = EMAFAST - EMASLOW
    DEA_ = EMA(DIFF, MID)
    MACD = (DIFF - DEA_) * 2    
    DICT = {'DIFF': DIFF, 'DEA': DEA_, 'MACD': MACD}

    return pd.DataFrame(DICT)


def KDJ(DF, N, M1, M2):
    C = DF['Close']
    H = DF['High']
    L = DF['Low']

    RSV = (C - LLV(L, N)) / (HHV(H, N) - LLV(L, N)) * 100
    
    K = SMA(RSV, M1, 1)
    D = SMA(K, M2, 1)
    J = 3 * K - 2 * D
    
    DICT = {'KDJ_K': K, 'KDJ_D': D, 'KDJ_J': J}
    
    return pd.DataFrame(DICT)


def OSC(DF, N, M):  # 变动速率线
    C = DF['Close']
    OS = (C - MA(C, N)) * 100
    MAOSC = EMA(OS, M)
    DICT = {'OSC': OS, 'MAOSC': MAOSC}

    return pd.DataFrame(DICT)


def BBI(DF, N1, N2, N3, N4):  # 多空指标
    C = DF['Close']
    bbi = (MA(C, N1) + MA(C, N2) + MA(C, N3) + MA(C, N4)) / 4
    DICT = {'BBI': bbi}

    return pd.DataFrame(DICT)


def BBIBOLL(DF, N1, N2, N3, N4, N, M):  # 多空布林线
    bbiboll = BBI(DF, N1, N2, N3, N4)
    UPER = bbiboll + M * STD(bbiboll, N)
    DOWN = bbiboll - M * STD(bbiboll, N)
    DICT = {'BBIBOLL': bbiboll, 'UPER': UPER, 'DOWN': DOWN}

    return pd.DataFrame(DICT)


def PBX(DF, N1, N2, N3, N4, N5, N6):  # 瀑布线
    C = DF['Close']
    PBX1 = (EMA(C, N1) + EMA(C, 2 * N1) + EMA(C, 4 * N1)) / 3
    PBX2 = (EMA(C, N2) + EMA(C, 2 * N2) + EMA(C, 4 * N2)) / 3
    PBX3 = (EMA(C, N3) + EMA(C, 2 * N3) + EMA(C, 4 * N3)) / 3
    PBX4 = (EMA(C, N4) + EMA(C, 2 * N4) + EMA(C, 4 * N4)) / 3
    PBX5 = (EMA(C, N5) + EMA(C, 2 * N5) + EMA(C, 4 * N5)) / 3
    PBX6 = (EMA(C, N6) + EMA(C, 2 * N6) + EMA(C, 4 * N6)) / 3
    DICT = {'PBX1': PBX1, 'PBX2': PBX2, 'PBX3': PBX3, 'PBX4': PBX4, 'PBX5': PBX5, 'PBX6': PBX6}

    return pd.DataFrame(DICT)


def BOLL(DF, N):  # 布林线
    C = DF['Close']
    boll = MA(C, N)
    UB = boll + 2 * STD(C, N)
    LB = boll - 2 * STD(C, N)
    DICT = {'BOLL': boll, 'UB': UB, 'LB': LB}

    return pd.DataFrame(DICT)


def ROC(DF, N, M):  # 变动率指标
    C = DF['Close']
    roc = 100 * (C - REF(C, N)) / REF(C, N)
    return pd.DataFrame({'ROC': roc, 'MAROC': MA(roc, M)})


def MTM(DF, N, M):  # 动量线
    C = DF['Close']
    mtm = C - REF(C, N)
    MTMMA = MA(mtm, M)
    DICT = {'MTM': mtm, 'MTMMA': MTMMA}

    return pd.DataFrame(DICT)


def MFI(DF, N):  # 资金指标
    C = DF['Close']
    H = DF['High']
    L = DF['Low']
    VOL = DF['Volume']
    TYP = (C + H + L) / 3
    V1 = SUM(IF(TYP > REF(TYP, 1), TYP * VOL, 0), N) / SUM(IF(TYP < REF(TYP, 1), TYP * VOL, 0), N)
    mfi = 100 - (100 / (1 + V1))
    DICT = {'MFI': mfi}

    return pd.DataFrame(DICT)


def SKDJ(DF, N, M):
    CLOSE = DF['Close']
    LOWV = LLV(DF['Low'], N)
    HIGHV = HHV(DF['High'], N)
    RSV = EMA((CLOSE - LOWV) / (HIGHV - LOWV) * 100, M)
    K = EMA(RSV, M)
    D = MA(K, M)
    DICT = {'SKDJ_K': K, 'SKDJ_D': D}

    return pd.DataFrame(DICT)


def WR(DF, N, N1):  # 威廉指标
    HIGH = DF['High']
    LOW = DF['Low']
    CLOSE = DF['close']
    WR1 = 100 * (HHV(HIGH, N) - CLOSE) / (HHV(HIGH, N) - LLV(LOW, N))
    WR2 = 100 * (HHV(HIGH, N1) - CLOSE) / (HHV(HIGH, N1) - LLV(LOW, N1))
    DICT = {'WR1': WR1, 'WR2': WR2}

    return pd.DataFrame(DICT)


def BIAS(DF, N1, N2, N3):  # 乖离率
    CLOSE = DF['Close']
    BIAS1 = (CLOSE - MA(CLOSE, N1)) / MA(CLOSE, N1) * 100
    BIAS2 = (CLOSE - MA(CLOSE, N2)) / MA(CLOSE, N2) * 100
    BIAS3 = (CLOSE - MA(CLOSE, N3)) / MA(CLOSE, N3) * 100
    DICT = {'BIAS1': BIAS1, 'BIAS2': BIAS2, 'BIAS3': BIAS3}

    return pd.DataFrame(DICT)


def RSI(DF, N1, N2, N3):  # 相对强弱指标RSI1:SMA(MAX(CLOSE-LC,0),N1,1)/SMA(ABS(CLOSE-LC),N1,1)*100;
    CLOSE = DF['Close']
    LC = REF(CLOSE, 1)
    RSI1 = SMA(MAX(CLOSE - LC, 0), N1, 1) / SMA(ABS(CLOSE - LC), N1, 1) * 100
    RSI2 = SMA(MAX(CLOSE - LC, 0), N2, 1) / SMA(ABS(CLOSE - LC), N2, 1) * 100
    RSI3 = SMA(MAX(CLOSE - LC, 0), N3, 1) / SMA(ABS(CLOSE - LC), N3, 1) * 100
    DICT = {'RSI1': RSI1, 'RSI2': RSI2, 'RSI3': RSI3}

    return pd.DataFrame(DICT)


def ADTM(DF, N, M):  # 动态买卖气指标
    HIGH = DF['High']
    LOW = DF['Low']
    OPEN = DF['Open']
    DTM = IF(OPEN <= REF(OPEN, 1), 0, MAX((HIGH - OPEN), (OPEN - REF(OPEN, 1))))
    DBM = IF(OPEN >= REF(OPEN, 1), 0, MAX((OPEN - LOW), (OPEN - REF(OPEN, 1))))
    STM = SUM(DTM, N)
    SBM = SUM(DBM, N)
    ADTM1 = IF(STM > SBM, (STM - SBM) / STM, IF(STM == SBM, 0, (STM - SBM) / SBM))
    MAADTM = MA(ADTM1, M)
    DICT = {'ADTM': ADTM1, 'MAADTM': MAADTM}

    return pd.DataFrame(DICT)

def ENE(DF, N=10, M1=11, M2=9):
    CLOSE = DF['Close']
    UPPER = (1 + M1 / 100) * MA(CLOSE, N);
    LOWER = (1 - M2 / 100) * MA(CLOSE, N);
    ene = (UPPER + LOWER) / 2;

    return pd.DataFrame({'UPPER': UPPER, 'LOWER': LOWER, 'ENE': ene})

def DDI(DF, N, N1, M, M1):  # 方向标准离差指数
    H = DF['High']
    L = DF['Low']

    DMZ = IF((H + L) <= (REF(H, 1) + REF(L, 1)), 0, MAX(ABS(H - REF(H, 1)), ABS(L - REF(L, 1))))
    DMF = IF((H + L) >= (REF(H, 1) + REF(L, 1)), 0, MAX(ABS(H - REF(H, 1)), ABS(L - REF(L, 1))))
    DIZ = SUM(DMZ, N) / (SUM(DMZ, N) + SUM(DMF, N))
    DIF = SUM(DMF, N) / (SUM(DMF, N) + SUM(DMZ, N))
    ddi = DIZ - DIF

    AD = MA(ADDI, M1)
    
    ADDI = SMA(ddi, N1, M)
    DICT = {'DDI': ddi, 'ADDI': ADDI, 'AD': AD}

    return pd.DataFrame(DICT)
