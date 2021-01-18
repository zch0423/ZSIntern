#%%
import pandas as pd
import numpy as np
filePath = "propertyROE-.xlsx"
data = pd.read_excel(filePath)

#%%
# 一季
column1 = [4*n+2 for n in range(21)]
column1 = [0, 1]+column1
# 中期
columnM = [4*n+3 for n in range(21)]
columnM = [0, 1]+columnM
# 三季
column3 = [4*n+4 for n in range(21)]
column3 = [0, 1]+column3
# 年报
columnA = [4*n+5 for n in range(21)]
columnA = [0, 1]+columnA

# %%
def filterST(x):
    if isinstance(x, float):
        return False  # NaN
    if x.startswith("*ST") or x.startswith("ST"):
        return False
    return True
data = data[data.iloc[:,1].apply(lambda x:filterST(x))]

# %%
columns = ["code", "name"]
for i in range(2000, 2021):
    columns.append(str(i)+"S1")
    columns.append(str(i)+"S2")
    columns.append(str(i)+"S3")
    columns.append(str(i)+"S4")

#%%
data.columns = columns
#%%
data1 = data.iloc[:,column1]
dataM = data.iloc[:,columnM]
data3 = data.iloc[:, column3]
dataA = data.iloc[:,columnA]

# %%
data1
# %%
data.to_excel("propertyNoST.xlsx", index=False)
# %%
data1.to_excel("propertyS1.xlsx")
dataM.to_excel("propertyS2.xlsx")
data3.to_excel("propertyS3.xlsx")
dataA.to_excel("propertyS4.xlsx")
# %%
