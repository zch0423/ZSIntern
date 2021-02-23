# coding:utf-8
'''
    FileName      ：roeProcessTools.py
    Author        ：@zch0423
    Date          ：Jan 19, 2021
    Description   ：
    - 处理数据
        - 去除ST
        - 更改列名
        - 去除全为空的列
        - 去除不连续的公司
        - 导出数据，roeData.xlsx
        - winsorize
        - 去除数据不超过minNum的公司，minNum=40
        - 导出数据，winsorized.xlsx
    - 计算行业标准差，取得波动大于行业标准差的公司，roeStd，导出数据，
    - 从roeStd中再根据规则筛选出good，规则如超过n个std的比例超过proportion
    - 对good进行mark，导出mark数据
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import scipy.signal as signal
from matplotlib.font_manager import FontProperties
zhfont = FontProperties(fname="/System/Library/Fonts/PingFang.ttc")


def getNameByCode(code, data):
    '''
    Description:
    根据code获取name
    ---
    Params:
    code, string
    data, DataFrame
    ---
    Returns:
    name, String
    '''
    company = data[data["code"].str.contains(code)]
    return company.name.values[0]


def getCompanyByCode(code, data):
    '''
    Description:
    根据code获取公司DataFrame数据以及y值
    ---
    Params:
    code, String
    data, DataFrame
    ---
    Returns:
    company, DataFrame, 只有一行
    y, Series
    '''
    company = data[data["code"].str.contains(code)]
    y = company.iloc[0, 2:]
    return company, y


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


def preProcess(data, startYear=2000, endYear=2021):
    '''
    Description:
    - 去除ST
    - 更改列名
    - 去除全为空的列
    - 去除不连续的公司 
    ---
    Params:
    data, DataFrame, raw data
    startYear, int default 2000
    endYear, int default 2021
    ---
    Returns:
    DataFrame, pre-processed data
    '''
    # 更改列名
    columns = ["code", "name"]
    for year in range(startYear, endYear):
        for month in range(3, 13, 3):  # 3 6 9 12
            columns.append("%d-%02d" % (year, month))
    data.columns = columns 

    # 去除空行
    data = data[~(data["name"].isnull())]
    # 去除ST
    data = data[~data["name"].str.contains("ST")]
    # 去除全为空的列，即没有数据的年份
    data.dropna(how="all", axis=1, inplace=True)
    # 去除近年没有数据的公司
    # 不能用最后一列，改用后两列
    c1 = data.columns[-1]
    c2 = data.columns[-2]
    data = data[~((data[c1].isnull())&(data[c2].isnull()))] 
    # 去除不连续的公司，空缺roe不超过1
    data = data[data.apply(lambda x:isContinuous(x), axis=1)]
    return data


def winsorize(data, winsorizeBool=True):
    '''
    Description:
    - winsorize
    ---
    Params:
    data, DataFrame
    winsorizeBool, bool default True
    ---
    Returns:
    DataFrame
    '''
    if winsorizeBool:
        data.iloc[:, 2:] = data.iloc[:, 2:].apply(lambda x: np.clip(
            x, np.nanquantile(x, 0.05), np.nanquantile(x, 0.95)), axis=1)
    return data


def removeLessThan(data, minNum=40):
    '''
    Description:
    去除比指定数据量少的公司
    ---
    Params:
    data, DataFrame
    minNum, int 40, 要求公司有的最少的数据列
    ---
    Returns:
    DataFrame
    '''
    # 原始包含code和name列
    return data[data.count(axis=1) > minNum+2]


def getYRolling(y, n=8, gaussian=True, center=True):
    '''
    Description:
    获取平滑后的曲线
    ---
    Params:
    y, Series, 原始y值
    n, int default 8, window size
    gaussian, bool default True, 高斯模糊还是简单加权平均
    center, bool default True, 计算平均居中还是靠右
    ---
    Returns:
    yRolling, Series 
    '''
    if gaussian:
        yRolling = y.rolling(n, win_type="gaussian",
                             center=center).mean(std=np.std(y, ddof=1))
    else:
        yRolling = y.rolling(n, center=center).mean()
    return yRolling


def greaterThanStd(data, n=8, gaussian=True, center=True):
    '''
    Description:
    是否比行业的标准差大，返回高于标准差的DataFrame
    ---
    Params:
    data, DataFrame, 行业数据
    ---
    Returns:
    DataFrame
    '''
    stds = []
    # for i in data.index:
    for code in data.code.values:
        company, y = getCompanyByCode(code, data)
        yRolling = getYRolling(y, n=n, gaussian=gaussian, center=center)
        stds.append(np.std(yRolling, ddof=1))
    avgStd = np.average(stds)
    return data[stds>avgStd]


def getExtreme(yRolling, order=4):
    '''
    Description:
    返回极值下标
    ---
    Params:
    yRolling, Series
    order, int default 4, 极值计算规则比相邻order要大
    ---
    Returns:
    maxIdx, minIdx, 下标
    '''
    y = np.array(yRolling[~yRolling.isnull()])  # 去除NaN不然可能在端点得不到极值
    maxIdx = signal.argrelextrema(y, np.greater_equal, order=order)[0]
    minIdx = signal.argrelextrema(y, np.less_equal, order=order)[0]
    return maxIdx, minIdx


def isGoodByRelDiff(maximum, minimum, std, n=1.5, minExtreme=4, proportion=0.2):
    '''
    Description:
    通过相对差值选择公司，极值个数不少于minExtreme，却存在超过n个std的极值差
    ---
    Params:
    maximum, Series, maximum points
    minimum, Series, minimum points
    std, float, std for yRolling
    n, float default 1.5, std times
    minExtreme, int default 4, number of minimum tolerant extreme points
    proportion, float default 0.2, 极值差超过n个std的比例
    ---
    Returns:
    bool, True means good 
    '''
    minMax = pd.concat([maximum, minimum]).sort_index()
    if len(minMax) < minExtreme:
        return False
    minMaxDiff = np.abs(minMax.diff(1))  # 相邻极值点的差值
    return (minMaxDiff >= n*std).sum() >= (proportion*(len(minMax)-1))


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
    return abs(p-minimum[-1]) < precision


def markCompany(yRolling, maximum, minimum, threshold=0.8, highPct=75):
    '''
    Description:
    标记公司
    ---
    Params:
    yRolling, Series, dropna already
    maximum, 极大值点
    minimum, 极小值点
    threshold, default 0.8, 上升幅度超过threhold
    highPct, default 75, 75分位点认为是高位
    ---
    Returns:
    mark, string
    '''
    pRoll = yRolling[-1]
    if not isMinimum(pRoll, maximum):
        return "非连续上升"
    high = np.percentile(yRolling, highPct)
    pMin = minimum[-1]
    if pMin > high:
        return "高位低点"
    # 上升超过threshold
    if pRoll - pMin < threshold:
        return "上升没超过阈值"
    return "I"


def mark(df, n=8, center=False, gaussian=True, order=4, threshold=0.8, highPct=75, increaseBool=True):
    '''
    Description:
    对DataFrame中所有公司进行标记，并返回标记和开始上升时间
    ---
    Params:
    n, int default 8, param for rolling
    center, bool default False, param for rolling
    gaussian, bool default True, gaussian filter or moving average
    order, int default 4, param for argrelextreme
    threshold, float default 0.8, threshold for increase
    highPct, int default 75, percentile for high threshold
    increaseBool, bool default True, whether only show increase marked companies
    ---
    Returns:
    DataFrame with four columns, code name mark startTime
    '''
    codes = df.code.values
    marks = []
    startTime = []
    for code in codes:
        company, y = getCompanyByCode(code, df)
        yRolling = getYRolling(y, n=n, gaussian=gaussian, center=center)
        yRolling.dropna(inplace=True)
        maxIdx, minIdx = getExtreme(yRolling, order=order)
        maximum, minimum = yRolling[maxIdx], yRolling[minIdx]
        marks.append(markCompany(yRolling, maximum, minimum))
        startTime.append(minimum.index[-1])
    temp = pd.DataFrame(data={"code": codes, "name": df.name.values, 
                        "mark": marks,  "startTime": startTime})
    return temp[temp["mark"]=="I"] if increaseBool else temp


# 暂时不用，效果不好
# def markCompany(pExtr, pRoll, pRoe, minimum, maximum):
#     '''
#     Description:
#     给公司标记
#     L, low, 低位
#     H, high, 高位
#     I, increase, 上升期
#     D, decrease, 下降期
#     ---
#     Params:
#     pExtr, float, last extreme point
#     pRoll, float, last point on the rolling series
#     pRoe, float, last roe data
#     minimum, Series, minimum points list
#     maximum, Series, maximum points list
#     ---
#     Returns:
#     mark, string, L H I D, 在中间的返回
#     '''
#     if isMinimum(pExtr, minimum):
#         # 判断是否是上升趋势，如果是下降趋势，则抛出异常
#         # 先判断极值点是否是平滑曲线最后的点
#         if isMinimum(pRoll, minimum):
#             if pRoe < pRoll:
#                 return "D"  # 最后一个是极小值
#             else:
#                 return "L/I"  # 不确定 低位或上升
#         if pRoll < pExtr:
#             raise ValueError("异常，小于极小值")
#         # pRoll > pExtr
#         if pRoe > pRoll:
#             return "I"
#         elif pRoe < pExtr:
#             return "L/D"  # 不确定 低位或继续下降
#         else:
#             return "L/I"  # 不确定 低位或上升
#     else:
#         if isMinimum(pRoll, maximum):
#             if pRoe > pRoll:
#                 return "I"
#             else:
#                 return "H/D"

#         if pRoll > pExtr:
#             raise ValueError("异常，大于极大值")
#         # pRoll<pExtr
#         if pRoe < pRoll:
#             return "D"
#         elif pRoe > pExtr:
#             return "H/I"  # 高位或继续上升
#         else:
#             return "H/D"  # 高位或下降


# def markCompanies(companies, order=4):
#     '''
#     Description:
#     给所有的公司标记，返回一个DataFrame包含code name mark
#     ---
#     Params:
#     companies, DataFrame, 差分公司roe数据
#     order, int default 4
#     ---
#     Returns:
#     marked, DataFrame, columns = [code name mark]
#     '''
#     marks = []
#     codes = companies.code.values
#     names = companies.name.values
#     for code in codes:
#         company, y = getCompanyByCode(code, companies)
#         yRolling = getYRolling(y)
#         yRolling = yRolling[~yRolling.isnull()]
#         maxIdx, minIdx = getExtreme(yRolling, order=order)
#         maximum, minimum = yRolling[maxIdx], yRolling[minIdx]
#         minMax = pd.concat([maximum, minimum]).sort_index()
#         pExtr = minMax[-1]
#         pRoll = yRolling[-1]  # 最后一个rolling
#         pRoe = company.iloc[0, -1]  # roe 数据中最后一个点
#         #TODO 没有ValueError
#         try:
#             marks.append(markCompany(pExtr, pRoll, pRoe, minimum, maximum))
#         except ValueError:
#             marks.append("")
#             print(company.iloc[0, :2])
#     return pd.DataFrame(data={"code": codes, "name": names, "mark": marks})


def drawROEandExtreme(maxs, mins, y, yRolling, company, minBool=True, maxBool=True, roeBool=True, mark=None):
    '''
    Description:
    绘制ROE，平滑线和标注极点
    ---
    Params:
    maxs, Series, 极大值点
    mins, Series, 极小值点
    y, Series
    yRolling, Series
    company, 公司的DataFrame，只有一行
    minBool, bool default True, 是否标注极小值
    maxBool, bool default True, 是否标注极大值
    roeBool, bool default True, 是否显示roe
    mark, default None, 如果有传入为标记上升或下降
    ---
    Returns:
    '''
    fig, axs = plt.subplots(figsize=(12, 5))
    
    # y = company.iloc[0, 2:]
    if roeBool:
        x = [datetime.strptime(d, '%Y-%m').date() for d in company.columns[2:]]
        axs.plot(x, y, label="roe")
    xRoll = [datetime.strptime(d, '%Y-%m').date() for d in yRolling.index]
    axs.plot(xRoll, yRolling, label="roll")
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
    title = company.iloc[0, 0]+"  "+company.iloc[0, 1]
    if mark:
        title += "  "+mark
    axs.set_title(title, fontproperties=zhfont)  # code
    axs.legend()


def showOne(code, data, marked=None, n=8, gaussian=True, center=True, order=4, maxBool=True, minBool=True, roeBool=True):
    '''
    Description:
    根据code绘制某一公司的roe，趋势以及极值点，为drawROEandExtreme的封装
    Jan 20, 2021 16:30
    增加了mark标注在title上
    ---
    Params:
    code, string
    data, DataFrame
    ---
    Returns:
    '''
    company, y = getCompanyByCode(code, data)
    yRolling = getYRolling(y, n=n, gaussian=gaussian, center=center)
    yRolling = yRolling[~yRolling.isnull()]
    maximum, minimum = getExtreme(yRolling, order)
    maxs, mins = yRolling[maximum], yRolling[minimum]
    mark = None
    if marked is not None:
        _, mark = getCompanyByCode(code, marked)
        mark = mark[0]
    drawROEandExtreme(maxs, mins, y, yRolling, company,
                      maxBool, minBool, roeBool, mark)


def selectGood(data, n=1.5, minExtreme=4, proportion=0.2):
    '''
    Description:
    根据极值差超过n个均值的比例，极值点的个数筛选出好的公司
    ---
    Params:
    data, DataFrame
    ---
    Returns:
    goodDf, DataFrame
    '''
    goodOrNots = []
    codes = data.code.values
    for code in codes:
        company, y = getCompanyByCode(code, data)
        yRolling = getYRolling(y)
        yRolling = yRolling[~yRolling.isnull()]
        maxIdx, minIdx = getExtreme(yRolling)
        maximum, minimum = yRolling[maxIdx], yRolling[minIdx]
        std = np.std(yRolling, ddof=1)
        goodOrNots.append(isGoodByRelDiff(maximum, minimum, std,
                                        n=n, minExtreme=minExtreme, proportion=proportion))
    return data[goodOrNots]


def clean(data, startYear=2000, endYear=2021, minNum=32, winsorizeBool=True):
    '''
    Description:
    数据处理的封装
    清洗数据，返回winsorized之后的数据
    ---
    Params:
    data, DataFrame
    startYear, endYear, minNum, winsorizeBool
    ---
    Returns:
    DataFrame
    '''
    data = preProcess(data, startYear=startYear, endYear=endYear)
    data = removeLessThan(data, minNum=minNum)
    data = winsorize(data, winsorizeBool=winsorizeBool)
    return data


def main(filePath, export=False, dirPath="test"):
    '''
    Description: test function
    ---
    Params:
    filePath, wind下载的原始数据
    export, bool default False, 是否导出
    dirPath, string default test, endswith /, 导出文件夹目录
    ---
    Returns:
    '''
    if export:
        if not dirPath.endswith("/"):
            dirPath += "/"
    # 数据预处理
    data = pd.read_excel(filePath)
    data = preProcess(data, startYear=2000, endYear=2021)
    if export:
        data.to_excel(f"{dirPath}roeData.xlsx", index=False)
    data = removeLessThan(data, minNum=40)
    if export:
        data.to_excel(f"{dirPath}预处理暂存.xlsx", index=False)
    data = winsorize(data, winsorizeBool=True)
    if export:
        data.to_excel(f"{dirPath}winsorized.xlsx", index=False)


    # 比行业均值大的
    data = greaterThanStd(data, n=8, gaussian=True, center=True)
    if export:
        data.to_excel(f"{dirPath}gStd.xlsx", index=False)
    # 选择具有周期性波动的公司
    selected = selectGood(data, n=1.5, minExtreme=4, proportion=0.2) 
    print("共筛选出%d个公司"%len(selected))
    if export:
        selected.to_excel(f"{dirPath}selected.xlsx", index=False)
    marked = markCompanies(selected)
    if export:
        marked.to_excel(f"{dirPath}marked.xlsx", index=False)

if __name__ == '__main__':
    filePath = "Jan14/机械设备roe单季度.xlsx"
    main(filePath, export=True, dirPath="test/")
