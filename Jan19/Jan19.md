Jan 19, 2021 16:01

判定改进思路

不只用最后一季度的roe，尝试改用最后几个季度的roe数据短期的消除干扰？

可以用历史的数据来判定是否有效

- 比如已经知道2011-2016一直在跌，那么用2011为止的数据，给定2012，2013判定是否在跌

需要判定的点离极值点越靠近，则确定性越弱；但离得越远，及时性不足

- 确定性和及时性似乎不可兼得，如何balance？



Jan 19, 2021 15:51

化工行业

002037.SZ 判定是在高位，但从长时间跨度来看应该是在低位？

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210119155135067.png" alt="image-20210119155135067" style="zoom:50%;" />





人为缩短时间跨度，测试能不能较早找到

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210119155403070.png" alt="image-20210119155403070" style="zoom:50%;" />



<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210119155528166.png" alt="image-20210119155528166" style="zoom:50%;" />











---

- winsorizedRoe.xlsx，初步筛选过的roe数据
    - 无ST
    - 去除空列
    - 5-95 winsorized
    - 去除不连续
- roeMarked 根据绝对规则筛选roe的结果，obsolete
- diffMarked 差分结果, obsolete
- std2p02.xlsx☑️
    - 按高于2个std且比例超过0.2筛选后的公司mark



## mark结果部分展示

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210119132131403.png" alt="image-20210119132131403" style="zoom:50%;" />

中联重科，Increase

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210119132204876.png" alt="image-20210119132204876" style="zoom:50%;" />

哈工智能，Decrease

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210119132705006.png" alt="image-20210119132705006" style="zoom:50%;" />

达意隆，High





## 是否用差分数据  x不用

上图是未差分得出是I上升，

下图是差分后数据，得出是D下降，相反

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210119093908213.png" alt="image-20210119093908213" style="zoom:50%;" />

用ROE数据筛选和用差分数据筛选得到的结果不一致，有一些公司可能只出现在一个地方

