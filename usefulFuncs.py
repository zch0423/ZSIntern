#coding:utf-8
'''
    FileName      ：usefulFuncs.py
    Author        ：@zch0423
    Date          ：Jan 18, 2021
    Description   ：
    一些常用的函数定义
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import scipy.signal as signal
from random import sample, randint
from scipy.stats.mstats import winsorize

def getNameByCode(code, data):
    '''
    code, data
    '''
    company = data[data["code"].str.contains(code)]
    return company.name.values[0]
    

def getCompanyByCode(code, data):
    '''
    code, data; company, df; y, series
    '''
    company = data[data["code"].str.contains(code)]
    y = company.iloc[0, 2:]
    return company, y


def getYRolling(y, n=8, gaussian=True, center=True):
    '''
    获取滚动值，y series roe数据
    '''
    if gaussian:
        yRolling = y.rolling(n, win_type="gaussian",
                             center=center).mean(std=np.std(y, ddof=1))
    else:
        yRolling = y.rolling(n, center=center).mean()
    return yRolling


def getExtreme(yRolling, order=3):
    '''
    返回极值下标
    '''
    y = np.array(yRolling)
    maximum = signal.argrelextrema(y, np.greater_equal, order=order)[0]
    minimum = signal.argrelextrema(y, np.less_equal, order=order)[0]
    return maximum, minimum


def drawROEandExtreme(maxs, mins, y, yRolling, company, minBool=True, maxBool=True, roeBool=True):
    '''
    绘制roe和极点, company, df 只有一行
    '''
    fig, axs = plt.subplots(figsize=(12, 5))
    x = [datetime.strptime(d, '%Y-%m').date() for d in company.columns[2:]]
    # y = company.iloc[0, 2:]
    if roeBool:
        axs.plot(x, y, label="roe")
    axs.plot(x, yRolling, label="roll")
    xMax = [datetime.strptime(d, '%Y-%m').date() for d in maxs.index]
    xMin = [datetime.strptime(d, '%Y-%m').date() for d in mins.index]
    axs.scatter(xMax, maxs, label="max", c='r')
    axs.scatter(xMin, mins, label="min", c='g')
    if maxBool:
        for i, tempX in enumerate(xMax):
            axs.annotate(str(tempX)[:-3], xy=(tempX, maxs[i]+0.1), c="r")
    if minBool:
        for i, tempX in enumerate(xMin):
            axs.annotate(str(tempX)[:-3], xy=(tempX, mins[i]-0.1), c="g")
    axs.set_title(company.iloc[0, 0])  # code
    fig.legend()


def pickOne(data):
    one = randint(0, len(data)-1)
    companyCode = data.iloc[one, 0]
    companyName = data.iloc[one, 1]
    return companyCode, companyName


def showOne(code, data, n=8, gaussian=True, center=True, order=3, maxBool=True, minBool=True, roeBool=True):
    company, y = getCompanyByCode(code, data)
    yRolling = getYRolling(y, n=n, gaussian=gaussian, center=center)
    maximum, minimum = getExtreme(yRolling, order)
    maxs, mins = yRolling[maximum], yRolling[minimum]
    drawROEandExtreme(maxs, mins, y, yRolling, company,
                      maxBool, minBool, roeBool)


def isGoodByAbsDiff(maxs, mins, absDiff=2, threshold=0.3):
    '''
    Description:
    根据极大极小值的绝对差值来判定
    ---
    Params:
    maxs, Series, maximum values, index-datetime
    mins, Series, minimum values, index-datetime
    absDiff, float, default 2, threshold for difference between adjacent maximum and minimum value
    threshold, float, default 0.4, threshold for the proportion exceeding the absDiff
    ---
    Returns:
    bool, True means good company
    '''
    minMax = pd.concat([maxs, mins]).sort_index()
    minMaxDiff = np.abs(minMax.diff(1))  # 相邻极值点的差值
    # print(minMaxDiff)
    return (minMaxDiff > absDiff).sum() > threshold*(len(minMaxDiff)-1)


def isGoodByRelDiff(maximum, minimum, std, n=1.5, minExtreme=4, proportion=0.5):
    '''
    Description:
    通过相对差值选择公司，极值个数不少于minExtreme，却存在超过n个std的极值差
    ---
    Params:
    maximum, Series, maximum points
    minimum, Series, minimum points
    std, float, std for yRolling
    n, float, std times
    minExtreme, int, number of minimum tolerant extreme points
    proportion, float, 极值差超过n个std的比例
    ---
    Returns:
    bool, True means good 
    '''
    minMax = pd.concat([maximum, minimum]).sort_index()
    if len(minMax) < minExtreme:
        return False
    minMaxDiff = np.abs(minMax.diff(1))  # 相邻极值点的差值
    return (minMaxDiff >= n*std).sum() >= (proportion*(len(minMax)-1))


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


def selectCompanyByAbsDiff(diff, absDiff=1.7, threshold=0.3, order=3, minNum=40, minExtreme=4, winsorize=True):
    '''
    Description:
    根据绝对差值选择公司并导出
    ---
    Params:
    diff, DataFrame, one difference data
    absDiff, float default 1.7
    threshold, float default 0.3, proportion threshold
    order, int default 3, order for guassian filter
    minNum, int default 40, minimum row number for required data
    minExtreme, int default 4, minimum tolerance for existing extreme points
    winsorize, bool default True, winsorize to (0.05, 0.95)
    ---
    Returns:
    goodCodes, list, codes for good companies
    temp, df, after winsorized and so on
    '''
    temp = diff.copy()
    # drop year with all being NaN
    temp.dropna(axis=1, how="all", inplace=True)
    # 至少有minNum个季度
    temp = temp[temp.count(axis=1) > minNum]
    # ROE 数据连续
    temp = temp[temp.apply(lambda x:isContinuous(x), axis=1)]
    # 缩尾
    if winsorize:
        temp.iloc[:, 2:] = temp.iloc[:, 2:].apply(lambda x: np.clip(
            x, np.nanquantile(x, 0.05), np.nanquantile(x, 0.95)), axis=1)
    codes = temp["code"].values
    goodCodes = []
    for code in codes:
        company, y = getCompanyByCode(code, temp)
        yRolling = getYRolling(y)
        # if yRolling.count()<minNum:
        #     continue
        maxIdx, minIdx = getExtreme(yRolling, order=order)
        if len(maxIdx)+len(minIdx) < minExtreme:
            continue
        maxs, mins = yRolling[maxIdx], yRolling[minIdx]
        if isGoodByAbsDiff(maxs, mins, absDiff=absDiff, threshold=threshold):
            goodCodes.append(code)
    return goodCodes, temp


def isMinimum(p, minimum, precision=1e-4):
    '''
    Description:
    判断极值点是不是极小值
    ---
    Params:
    p, float
    minimum, Series, 比较最后一个是不是极小值
    ---
    Returns:
    bool, True means is minimum
    '''
    return abs(p-minimum[-1])<precision


def markCompany(pExtr, pRoll, pRoe, minimum):
    '''
    Description:
    给公司标记
    L, low, 低位
    H, high, 高位
    I, increase, 上升期
    D, decrease, 下降期
    ---
    Params:
    pExtr, float, last extreme point
    pRoll, float, last point on the rolling series
    pRoe, float, last roe data
    minimum, Series, minimum points list
    ---
    Returns:
    mark, string, L H I D, 在中间的返回I* D*
    '''
    if isMinimum(pExtr, minimum):
       # 判断是否是上升趋势，如果是下降趋势，则抛出异常
        if pRoll < pExtr:
            raise ValueError("异常")
        # pRoll > pExtr
        if pRoe > pRoll:
            return "I"
        elif pRoe < pExtr:
            return "L"
        else:
            return "I*"
    else:
        if pRoll > pExtr:
            raise ValueError("异常")
        # pRoll<pExtr
        if pRoe < pRoll:
            return "D"
        elif pRoe > pExtr:
            return "H"
        else:
            return "D*"


def markCompanies(companies):
    '''
    Description:
    给所有的公司标记，返回一个DataFrame包含code name mark
    ---
    Params:
    companies, DataFrame, 差分公司roe数据
    ---
    Returns:
    marked, DataFrame, columns = [code name mark]
    '''
    marks = []
    codes = companies.code.values
    names = companies.name.values
    for code in codes:
        company, y = getCompanyByCode(code, companies)
        yRolling = getYRolling(y)
        maxIdx, minIdx = getExtreme(yRolling, order=3)
        maximum, minimum = yRolling[maxIdx], yRolling[minIdx]
        minMax = pd.concat([maximum, minimum]).sort_index()
        pExtr = minMax[-1]
        pRoll = yRolling[~yRolling.isnull()][-1]  # 最后一个rolling
        pRoe = company.iloc[0, -1]  # roe 数据中最后一个点
        #TODO 没有ValueError
        # try:
        marks.append(markCompany(pExtr, pRoll, pRoe, minimum))
        # except ValueError:
        # marks.append("")
        # print(company.iloc[0, :2])
    return pd.DataFrame(data={"code":codes, "name":names, "mark":marks})

def main(path):
    diff = pd.read_excel(path)  # 处理过的差分数据，包括winsorize等
    df = markCompanies(diff)
    # print(df)
    df.to_excel("Jan18/marked.xlsx", index=False)

if __name__ == "__main__":
    main("Jan18/temp58Good.xlsx")

