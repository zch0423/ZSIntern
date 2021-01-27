# Jan 26, 2021 09:14
1. 筛选
2. 预测

不能用指数平均，无法消除季节性影响

## 思路

### 1 趋势预测

仿照MACD用指数移动平均

以四川美丰为例

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210126110821946.png" alt="image-20210126110821946" style="zoom:50%;" />



分别用span=4，和span=8的ema可以看出末尾已经有抬头上升的趋势

我们关心什么时候ema从下穿过ema8，则认为其处于上升趋势

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210126110738976.png" alt="image-20210126110738976" style="zoom:50%;" />

dif = ema(4)-ema(8)

dem = ema(4, dif)

osc = dif-dem

osc由负转正是上升信号，用连续两个季度上升判定？由负转正后至少n个季度维持正 n=2?

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210126131617026.png" alt="image-20210126131617026" style="zoom:50%;" />

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210126131733291.png" alt="image-20210126131733291" style="zoom:50%;" />

问题，不够平滑？只是衡量短期的小趋势？



### 2 低位判断

1. percentile(10～35)





## ~~思路~~
~~先筛选再根据筛选的预测~~
很可能走不通

- ~~我们想要筛选出具有一定周期性波动特征的公司，但这种周期性并不是严格意义上的周期~~
- ~~暂时没有办法写出明确的规则，更多是靠人眼直观感觉“存在趋势”~~

## 思路
先预测再筛选
我们想要的是低位刚反弹、低位、高位反弹、高位的公司，可以同统一的规则预测后再取出是这四种标记的公司再进行人工的检验

- 涉及到预测规则的判定
- 考虑因素，即输入参数应该包含什么
    - 极值
    - 趋势
    - 时间跨度
    - 差值
    - ...

### 2.1 根据规则判断
人工决策树
- 人做出判断的规则界定，给出每一个清晰的条件

输入参数界定，主要解决两个方面问题
- 如何判断是低位
    - 寻找极小值点，是否是处于历史低位（用分位数衡量25%？）
    - 其他方法
- 如何判断反弹
    - 简单方法，用均线，认为连续n个季度抬升即反弹，n=2

### ~~2.2 时间序列回归ARIMA~~
不太现实，每个的AR和MA阶数需要确定

### 2.3 机器学习算法？
能想到的比较贴近的有决策树或者贝叶斯网络
但需要解决数据集标记的问题，人工需要判断一次