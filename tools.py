#coding=utf-8
'''
    FileName      ：tools.py
    Author        ：@zch0423
    Date          ：Mar 4, 2021
    Description   ：
    一些工具
    - getPriceData 从tushare获取股价
    - getEarlyTime 比较两个日期获取早的
    - correlate 返回roe或cf和price的pearson和spearman相关系数
'''
import pandas as pd
import numpy as np
from scipy.stats import spearmanr
import os
import tushare as ts
token = "a7c1312fe8187bff67ada6333c4b447caff18f58be66ac8b64d20d5a"
api = ts.pro_api(token)


def correlate(startTime: str, df: pd.DataFrame, price: pd.DataFrame) -> float:
    '''
    Description:
    根据startTime从df和price中获取开始时间之后的季度数据
    返回pearson相关系数和spearman相关系数及其pvalue
    ---
    Params:
    startTime, str, like "2014-01"
    df, DataFrame of only one row, company roe or cf data
    price, DataFrame, tushare 请求返回数据
    startTime, str, like 2014-01
    ---
    Returns:
    corrCoef, float 
    '''
    # 获取开始时间所在的下标
    timeIdx = df.columns.get_indexer([startTime, ])[0]
    data = df.iloc[0, timeIdx:]
    data.index = pd.to_datetime(data.index)
    # 转化成季度数据
    data = data.resample("Q").last()
    data.dropna(inplace=True)
    endTime = data.index[-1]
    # 获取价格的quarterly数据
    price["trade_date"] = pd.to_datetime(price["trade_date"], format="%Y%m%d")
    quarterly = price.resample("Q", on="trade_date").mean()
    price = quarterly[:endTime]["close"]
    temp = pd.DataFrame(data={"roe": pd.to_numeric(data), "close": price})
    temp.dropna(inplace=True)
    pearson = temp["roe"].corr(temp["close"])
    spearman = spearmanr(temp["roe"], temp["close"])
    return pearson, spearman

    
def getPriceData(code: str, startTime: str, endTime: str = "20201231", saveBool: bool = True):
    '''
    Description:
    根据code时间等从tushare获取股价信息
    ---
    Params:
    code, str
    startTime, str, like 2014-01
    endTime, str, like 20201231
    saveBool, bool, whether to save data as csv file, outfile named by code and starttime
    ---
    Returns:
    price
    '''
    outpath = f"data/{code[:-3]}-{startTime}.csv"
    if os.path.exists(outpath):
        # print("downloaded in", outpath)
        price = pd.read_csv(outpath)
        return price

    st = "".join(startTime.split("-"))+"01"
    price = ts.pro_bar(ts_code=code, adj='qfq',
                       start_date=st, end_date=endTime)
    if saveBool:
        if not os.path.exists("data/"):
            os.mkdir("data/")
        price.to_csv(outpath, index=False)
    return price


def getEarlyTime(time1: str, time2: str):
    '''
    Description:
    获取两个时间中较早的并返回
    ---
    Params:
    time, str, like 2014-01
    ---
    Returns:
    time, str, like 2014-01
    '''
    return time1 if time1 < time2 else time2
