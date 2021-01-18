# 文件说明
前复权是以当前价格修正之前的价格
- price处理后.xlsx 
    - 剔除了ST股票
- price15year.xlsx
    - 有超过15年的股价信息的公司，即60季度
- price59c.xlsx 
    - 在上面的基础上剔除了潍柴重机000880.SZ
    - 中间停了一年
- 机械roeData.xlsx
    - 剔除了ST修改了列名
- filteredROE.xlsx
    - 根据price的59家公司选出roe
- diffROE59.xlsx
    - 59家公司roe的4阶差分数据，去除季节性

# 程序说明
- process.ipynb
    - 主要处理roe数据
- processPrice.ipynb
    - 主要处理股价数据
- pattern.ipynb
    - 主要roe和股价观察相关性

