- [ ] 去除噪点，如何设置阈值
- [ ] 是否差分，应当要差分，但也存在差分后噪点变多的情况
- [ ] 筛选有效的公司，如何衡量有效

- 噪点
    - 平均的基础上再做一次平滑处理，更滞后
    - 一段时间内的波动设置阈值，在一段范围内只取一个点
    - 



## 1 处理噪点

order=1, 差分数据

取极值的时候设置order=3

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210115130856940.png" alt="image-20210115130856940" style="zoom:50%;" />

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210115131453283.png" alt="image-20210115131453283" style="zoom:50%;" />



## 2 筛选特征明显的公司

根据roe波动来筛选，倾向于筛选趋势明显即波动较大的

如果所有的相邻极大值和极小值没有超过n个标准差？就剔除？





















## 3  其他

## 有一些公司极点较突出

n=12

600528.SH 中铁工业

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210115101810959.png" alt="image-20210115101810959" style="zoom:50%;" />

### 差分不一定有效

中铁工业取n=8

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210115102038028.png" alt="image-20210115102038028" style="zoom:50%;" />

差分后

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210115102050170.png" alt="image-20210115102050170" style="zoom:50%;" />





差分前

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210115102220205.png" alt="image-20210115102220205" style="zoom:50%;" />

差分后

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210115102238757.png" alt="image-20210115102238757" style="zoom:50%;" />





## 一些公司不太有效

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210115101549278.png" alt="image-20210115101549278" style="zoom:50%;" />

![image-20210115105602627](/Users/zch/Library/Application Support/typora-user-images/image-20210115105602627.png)

