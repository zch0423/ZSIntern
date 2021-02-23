#coding=utf-8
'''
    FileName      ：cfProcessTools.py
    Author        ：@zch0423
    Date          ：Feb 23, 2021
    Description   ：
    处理现金流相关的函数
    - cleanCFData(df, startYear=2000, endYear=2021, minNum=32)
    - demoOne(company) 
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import scipy.signal as signal
from matplotlib.font_manager import FontProperties
zhfont = FontProperties(fname="/System/Library/Fonts/PingFang.ttc")


def isContinuous(x):
    '''
    Description:
    筛选出中断的公司，中断期不超过1
    ---
    Params:
    x, for df.apply(), a row Series
    ---
    Returns:
    bool, True 表示连续, False means discontinuity
    '''
    it = iter(x)
    # 确保有元素且不全为nan
    while isinstance(next(it), str):
        pass
    while np.isnan(next(it)):
        pass
    count = 0
    while True:
        try:
            temp = next(it)
            if np.isnan(temp):
                count += 1
                if count > 1:
                    return False
        except StopIteration:
            return True


def cleanCFData(df, startYear=2000, endYear=2021, minNum=32, continuousBool=True):
    '''
    Description:
    清洗现金流相关季度数据
    - 去除空行
    - 去除ST
    - 去除最近两季度没有数据的公司
    - 去除不连续公司
    - 去除数据量少于minNum的公司
    ---
    Params:
    startYear, default 2000
    endYear, default 2021
    minNum, default 32
    continuousBool, default True, remove incontinuous rows
    ---
    Returns:
    DataFrame
    '''
    columns = ["code", "name"]
    for year in range(startYear, endYear):
        for quarter in [3, 6, 9, 12]:
            columns.append(f"{year}-{quarter:02}")
    df.columns = columns
    # 去除ST
    df = df[~df["name"].str.contains("ST")]
    # 去除空行
    df = df[~df["name"].isnull()]
    # 去除全为空的列，即没有数据的年份
    df.dropna(how="all", axis=1, inplace=True)
    # 去除近年没有数据的公司
    # 不能用最后一列，改用后两列
    c1 = df.columns[-1]
    c2 = df.columns[-2]
    df = df[~((df[c1].isnull()) & (df[c2].isnull()))]
    if continuousBool:
        # 去除不连续的公司，空缺roe不超过1
        df = df[df.apply(lambda x:isContinuous(x), axis=1)]
    # 去除少于32季度数据的公司
    df = df[df.count(axis=1) > minNum+2]
    return df


def demoOne(company):
    '''
    Description:
    绘制一个公司的
    ---
    Params:
    company, 只有一行的DataFrame
    ---
    Returns:
    '''
    fig, axs = plt.subplots(figsize=(11, 5))
    x = [datetime.strptime(d, '%Y-%m').date() for d in company.columns[2:]]
    y = company.iloc[0, 2:]
    axs.plot(x, y, label="NetCF/Share")
    title = company.iloc[0, 0]+"  "+company.iloc[0, 1]
    axs.set_title(title, fontproperties=zhfont)  # code
    axs.legend()
