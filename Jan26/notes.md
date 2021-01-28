树回归/分段线性回归[树回归][https://blog.csdn.net/xieyan0811/article/details/78581974]

~~facebook prophet~~

## 解决思路 Jan 26, 2021 14:51

我们想要三种图形

- 先下降然后上升
- 先下降然后在低位波动
- 先下降然后在低位波动，然后上升

需要做的工作是识别三个部分

1. 先下降
2. 上升
3. 低位波动

==问题在时间跨度不知道==

### 下降的识别

如何找到下降的开始（==最重要==）

如何找到底部

找到开始和底部之后方便判断低位波动和上升识别



通过底部倒推？极小值点，~~判断是否处于低位（百分位）只要是就记录~~

~~（是否可以筛除泰山等公司？可能的去除逻辑：一大部分处于低位使其低位的百分比~~

判断是不在高位而不是在低位





### 上升的识别

从底部开始，移动平均线连续n个季度上升，认为是在上升



### 低位波动的识别

~~根据下降开始到底部差值，不超过0.1？认为是在波动~~

问题，以为是上升了，但马上下降了

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210126152020203.png" alt="image-20210126152020203" style="zoom:50%;" />

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210126152043268.png" alt="image-20210126152043268" style="zoom:50%;" />

或者直接将低位波动和上升一起识别（如果分不开的话











---

除了上升的判断还应该加入前面下降的判断

界定不想要的公司或者界定想要的公司

- 趋势明显，从低位反弹上升
- 极小值前没有频繁大小相差不大的极值交替，如泰山石油（自己写极值计算规则，比如极值应当超过某个阈值，不然维持不变



如果用现在的思路就不用minNum=32的限制

前面的数据其实没有用到，只用到了最近几期的数据

前面的数据可以用来算百分位

用百分位是不是比较粗糙，像泰山石油这种就判断不出来





## ~~另一个思路~~

~~用统计检验的方法~~

~~先选取近几年数据（那么之前就不需要进行筛选），判断是否存在趋势~~

~~如果有趋势，看是不是最近上升的趋势~~

- ~~找到极小值点，判断极小值点左边是不是下降趋势，右边是不是上升趋势，或者只看右边~~~

~~cox-stuart检验判断是否存在趋势，如果不存在趋势就是而在低位则是盘旋状态？好像不太行~~









## 无法去除下面这种公司

只用移动平均*center*=False, *gaussian*=False, *n*=4, *order*=2

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210126134909516.png" alt="image-20210126134909516" style="zoom:50%;" />

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210126135110090.png" alt="image-20210126135110090" style="zoom:50%;" />

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210126150603098.png" alt="image-20210126150603098" style="zoom:50%;" />



## 我们想要的公司

*center*=False, *gaussian*=False, *n*=8, *order*=2

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210126135215103.png" alt="image-20210126135215103" style="zoom:50%;" />

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210126135200537.png" alt="image-20210126135200537" style="zoom:50%;" />



<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210126135141335.png" alt="image-20210126135141335" style="zoom:50%;" />

