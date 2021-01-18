#%%
import matplotlib.dates as mdates
from matplotlib import ticker
import pandas as pd
import numpy as np
# %%
excelFile = "A股公司ROE趋势.xlsx"
# %%
data = pd.read_excel(excelFile)
# %%
data
# %%
def filterST(x):
    if isinstance(x, float):
        return False  # NaN
    if x.startswith("*ST") or x.startswith("ST"):
        return False
    return True
#%%
dataNoST = data[data["证券简称"].apply(lambda x:filterST(x))]
# %%
dataNoST
# %%
dataNoST.to_excel("noST.xlsx", index=False)
# %%
columns = ["证券代码", "证券简称"]
for i in range(2000, 2021):
    columns.append("ROE%d一季"%i)
    columns.append("ROE%d中报"%i)
    columns.append("ROE%d三季"%i)
    columns.append("ROE%d年报"%i)
# %%
columns
# %%
dataNoST.columns = columns
# %%
dataNoST
# %%
dataNoST.to_excel("noST1.xlsx", index=False)
# %%
import matplotlib.pyplot as plt
# %%
def drawOne(data):
    x = np.arange(2000, 2021)
    fig, axs = plt.subplots()
    axs.plot()
#%%
fig, axs = plt.subplots()
# %%
x = [i for i in range(2000, 2021)]
# %%
temp = dataNoST.loc[0,:]
# %%
column1 = [4*n+2 for n in range(21)]
# %%
temp1 = temp[column1]
# %%
temp1
# %%
axs.plot(x, temp1)
# %%
fig
# %%
axs.set_xlim(2000, 2021)
fig
# %%
axs.set_ylim(0, 2)
fig
# %%
axs.set_xlabel("year")
# %%
axs.set_ylabel("ROE")
# %%
from matplotlib import ticker
# %%
axs.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=2, decimals=1))
# %%
fig
# %%
# import matplotlib.dates as mdates
# axs.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

# %%
plt.xticks([i for i in range(2000, 2021)], [str(i) for i in range(2000, 2021)])
# %%

fig
# %%
def drawOne(y, axs):
    # fig, axs = plt.subplots()
    x = [i for i in range(2000, 2021)]
    axs.plot(x, y)
    axs.set_xlim(2000, 2021)
    axs.set_ylim(0, 2)
    axs.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=2, decimals=1))
    axs.set_xlabel("year")
    axs.set_ylabel("ROE")
# %%
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import ticker
data = pd.read_excel("noST1.xlsx")
# %%
# 一季

column1 = [4*n+2 for n in range(21)]
column1 = [0, 1]+column1
# 中期
columnM = [4*n+3 for n in range(21)]
columnM = [0, 1]+columnM
# 三季
column3 = [4*n+4 for n in range(21)]
column3 = [0,1]+column3
# 年报
columnA = [4*n+5 for n in range(21)]
columnA = [0,1 ]+columnA

# %%
temp = data.loc[0,:]
# %%
temp
# %%
temp1 = temp[column1]
tempM = temp[columnM]
temp3 = temp[column3]
tempA = temp[columnA]
# %%
tempA
# %%
fig, axs = plt.subplots()
x = [i for i in range(2000, 2021)]
axs.set_xlim(2000, 2021)
axs.set_ylim(0, 2)
# axs.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=3, decimals=1))
axs.set_xlabel("year")
axs.set_ylabel("ROE")
axs.plot(x, temp1, label="一季")
axs.plot(x, tempM, label="中期")
axs.plot(x, temp3, label="三季")
axs.plot(x, tempA, label="年报")
#%%
fig.legend()
# %%
fig
# %%
temp1
# %%
plt.plot(x, temp1)
# %%
plt.plot(x, )
# %%
for each in temp1:
    print(each)
# %%
data1 = data[column1]
# %%
column1
# %%
data
# %%
data1 = data.iloc[:, column1]
dataM = data.iloc[:, columnM]
# %%
data3 = data.iloc[:, column3]
dataA = data.iloc[:,columnA]
# %%
data1.to_excel("noST1.xlsx", index=False)
dataM.to_excel("noSTM.xlsx", index=False)
data3.to_excel("noST3.xlsx", index=False)
dataA.to_excel("noSTA.xlsx", index=False)

# %%
data.to_excel("noST-.xlsx", index=False)
# %%
data
# %%
data1
# %%
