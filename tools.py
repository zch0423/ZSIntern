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
    - plotIt 绘制股价和roe关系，结合roeProcessTools使用
'''
from roeProcessTools import *
import pandas as pd
import numpy as np
from scipy.stats import spearmanr
import os
import tushare as ts
token = "your token here"
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


def plotIt(code, df: pd.DataFrame, mark: pd.DataFrame, title:str ="roe", startYear:str ="2012"):
    '''
    Description:
    绘制股价和roe或cf等数据的图表
    ---
    Params:
    df, DataFrame, roe 或cf数据
    mark, DataFrame, 标记数据
    title, str, 标记信息
    startYear, str default 2012, 开始绘制数据的年份
    ---
    Returns:
    '''
    # 获取时间信息
    markRow = mark[mark["code"].str.contains(code)]
    startTime_roe = markRow.iloc[0, 3]
    startTime_cf = markRow.iloc[0, 6]
    earlyTime = getEarlyTime(startTime_roe, startTime_cf)
    # 获取股价信息，注意股价文件放在data中
    price = getPriceData(code, earlyTime)
    price["trade_date"] = pd.to_datetime(price["trade_date"], format="%Y%m%d")
    yPrice = price["close"]
    xPrice = [each.date() for each in price["trade_date"]]
    # 获取公司数据信息，取year-03之后的数据
    company = df[df["code"].str.contains(code)]
    company = company.dropna(axis=1)
    idx = company.columns.get_indexer((f"{startYear}-03",))[0]
    temp = pd.concat([company.iloc[:, :2], company.iloc[:, idx:]], axis=1)
    fig, axs = showOne(code, temp, marked=title, center=False)
    ax2 = axs.twinx()
    ax2.plot(xPrice, yPrice, label="price", c="crimson")
    ax2.legend()
