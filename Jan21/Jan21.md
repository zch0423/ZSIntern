## Jan 21

- [ ] ==最主要找到低位波动和低位上升的公司==

- [ ] 检验分类标记好的有效性，Jan 20 尝试标记.ipynb

- [ ] 如何去除这一类公司

    <img src="/Users/zch/Library/Application Support/typora-user-images/image-20210121145557789.png" alt="image-20210121145557789" style="zoom:33%;" />

- [ ] 保留这一类公司

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210121150421390.png" alt="image-20210121150421390" style="zoom:33%;" />

如何衡量趋势是否有效？

FP FN的比例有多少，怎么衡量？还是回归到趋势的有效性如何判断















如果最后一个是极小值应该直接判断为下降，因为已经包含了最后一期roe的数据，而不是L/I





L/I也可以判断是否触底历史低位

下降过程中判断出是否触底历史低位 chem 200553.SZ 300107.SZ

上升过程中判断是否触顶历史高位 chem 600143.SH

- 如果判定为下降，再判断roe是否处于历史低位，如果是则判断为低位（触底）

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210121100359739.png" alt="image-20210121100359739" style="zoom:50%;" />

## example

**给出判断为H/D，但应该是缓慢上升中**

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210121102146195.png" alt="image-20210121102146195" style="zoom:50%;" />

**给出判断为L/D，但应该是处于高位，而且非常缓慢下降**

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210121101941102.png" alt="image-20210121101941102" style="zoom:50%;" />

**应该判断为上升，连续四个季度上升**

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210121103312381.png" alt="image-20210121103312381" style="zoom:50%;" />

季节性影响，如果最后一个是极大值点应该直接判定为上升，或者看是否触顶，是否直接用roll数据趋势更好

~~如果用差分数据的话，差分-平滑-找零点~~



如何消除季节性影响，最后一个roe数据怎么取





<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210121100750479.png" alt="image-20210121100750479" style="zoom:50%;" />

<img src="/Users/zch/Library/Application Support/typora-user-images/image-20210121100549026.png" alt="image-20210121100549026" style="zoom:50%;" />