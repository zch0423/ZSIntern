# Casual Code
## Jan 13
- [x] wind导出excel格式
- [x] ROE数据清洗和格式化
- [x] 数据可视化，相关性研究
## Jan 14
- [x] 清洗前复权股价数据
- [x] 股价与ROE数据结合可视化
- [x] 数据差分后对比
- [x] 简单回归分析
## Jan 15
- [x] 从差分数据提取趋势计算极值
- [x] 主要采用高斯模糊进行平滑化处理
## Jan 18
- [x] winsorize处理异常值
- [x] 用极值差值的绝对数值对公司进行筛选
- [x] 初步根据图像特征将公司分为高位、低位、上升、下降四类
## Jan 19
- [x] 还是改用原始roe而不用差分数据，平滑化相当于考虑了季节因素
- [x] 根据规则筛选出波动性大的公司
- [x] 根据图像特征判断公司所处位置
- [x] 整理数据处理到mark思路
## Jan 20
- [x] 根据历史数据检查是否能及时判断下降和上升趋势
- [x] 公司标记规则再设置
- [x] 导出四个行业的清洗以及标记数据

## Jan 21
- [x] 检验标记数据
- [x] 修改标记规则，增加基于历史值的高位低位判断 
    - 效果不佳

## Jan 25
- [x] 根据数据数过滤chem，393-185
- [x] 时间序列平稳性过滤，185-153，效果不佳

