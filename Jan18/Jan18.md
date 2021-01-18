# Jan 18 Journal

- temp58Good.xlsx 包含了根据绝对差值选择出来的58家公司信息
- marked.xlsx 包含了初步标记信息
- classification.ipynb 主要是对数据进行处理以及公司筛选
- classification2.ipynb 主要是公司分类标记



## major task

### 1. 筛选公司

- 按绝对差值
- 两者结合？
- 删除中间出现空值的
- 异常值如何处理，进行5%-95%winsorize处理，np.clip()

1.  roe会受到异常值的影响，导致绝对差值很大，无法剔除，如下图两个公司

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210118110706350.png" alt="image-20210118110706350" style="zoom:50%;" />

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210118110811955.png" alt="image-20210118110811955" style="zoom:50%;" />



- 先程序筛选，剩下一部分再手动筛选  #TODO



### 2. 将公司分类

==可以考虑用每个公司的历史数据，根据历史数据特征来确定==  #TODO

- H，high
- L，low
- I，increase
- D，decrease

根据yRolling最后一个值和最近的极值点以及最近的roe三个点的位置关系，理论上共12种类型，但

极大值上升 p1<p2，极小值下降 p1>p2，没有发现

所以剩下6种类型

- 极大值下降
    - roe在下方
    - roe在中间
    - roe在上方
- 极小值上升
    - roe在上方
    - roe在中间
    - roe在下方

两者对称

极值点称为p1，yRolling最后一个平滑点为p2，最近的roe点为p3

### 1 极大值

#### 1.1 p1>p2>p3 下降期

300024.SZ

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210118153830909.png" alt="image-20210118153830909" style="zoom:50%;" />

最近的点为极大值，且平滑线下降，roe比平滑线最末还要低，可以确定处于下降期

#### 1.2 p1>p3>p2  倾向于认为处于下降期？

002430.SZ

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210118154822103.png" alt="image-20210118154822103" style="zoom:50%;" />



000528.SZ

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210118154142431.png" alt="image-20210118154142431" style="zoom:50%;" />

000821.SZ

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210118154231849.png" alt="image-20210118154231849" style="zoom:50%;" />



000852.SZ

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210118154318651.png" alt="image-20210118154318651" style="zoom:50%;" />



#### 1.3 p3>p1>p2 倾向于处于高位

900947.SH

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210118153545823.png" alt="image-20210118153545823" style="zoom:50%;" />

002009.SZ

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210118154510485.png" alt="image-20210118154510485" style="zoom:50%;" />

倾向于认为公司处于高位？确定性不如1.1

---

### 2 极小值

####  2.1 p1<p2<p3 上升期

002158.SZ

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210118154654732.png" alt="image-20210118154654732" style="zoom:50%;" />



和1.1对称

#### 2.2 p1<p3<p2 倾向于认为处于上升期

002526.SZ

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210118154922650.png" alt="image-20210118154922650" style="zoom:50%;" />





600218.SH

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210118153742793.png" alt="image-20210118153742793" style="zoom:50%;" />

000157.SZ

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210118154003820.png" alt="image-20210118154003820" style="zoom:50%;" />

002132.SZ

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210118154559653.png" alt="image-20210118154559653" style="zoom:50%;" />

#### 2.3 p3<p1<p2 倾向于处于低位

002337.SZ

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210118154737809.png" alt="image-20210118154737809" style="zoom:50%;" />

300080.SH

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210118154945012.png" alt="image-20210118154945012" style="zoom:50%;" />







#### 





### 3 异常

根据计算规则还没得出极值点，舍去

002438.SZ

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210118153928155.png" alt="image-20210118153928155" style="zoom:50%;" />

