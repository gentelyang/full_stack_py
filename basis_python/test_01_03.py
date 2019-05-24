#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:gentelyang  time:2019-05-23

#第一题：找到l1和l2中的相同值与不同值
# l1 = [11,22,33]
# l2 = [22,23,24]
# for i in l1:
#     if i in l2:
#         print "i为相同值",i
#     else:
#         print "i为不同值",i


#第二题：1,2,3,4,5,6,7,8,8个数字能组成多少个互不相同且无重复的数
# count = 0
# count_same = 0
# for i in range(1,9):
#     for j in range(1,9):
#         if i == j:
#             count_same += 1
#         count += 1
# print count - count_same

#第三题：99乘法表

# str1 = ""
# for i in range(1,10):
#     for j in range(1,i+1):
#         str1 +=str(i)+ "*" +str(j)+ "=" +str(i*j)+"\t"
#         # print "i*j=",i*j
#     print str1
#     str1 = ""#每个内循环结束后重新置为空
#另一个思路
# for i in range(1,10):
#     str1 = ""
#     for j in range(1,i+1):
#         str1 +=str(i) +"*"+str(j)+"="+str(i*j)+"\t"
#     print str1


#第四题：[1,2,3,4]组成两两不相同的数
# l1 = [1,2,3,4]
# for i in range(0,len(l1)-1):
#     for j in range(i+1,len(l1)):
#         print l1[i],l1[j]


#第五题：100文钱，公鸡5文一只，母鸡3文一只，小鸡3只一文，100文买100只鸡的可能方法
# for g in range(1,100//5):
#     for m in range(1,100//3):
#         for x in range(1,100):
#             if x + g + m == 100 and 5*g + 3*m + x/3 ==100:
#                 print g , m ,x

#第六题：利用下划线将列表中的元素拼接成一个字符串，li=["l","y","yang"]
# li = ["l","y","yang"]
# result = "_".join(li)#如果全是字符串可以用join拼接，但是如果有123这样的数字了就不能用join了
# print result
# li = ["l","y",123]
# str1 = ""
# for i in li:
#     str1 += str(i)
# result = "_".join(str1)
# print result

#第七题：
# tu = ("a","b","c")
# # # for id ,item in enumerate(tu):#默认的索引下标是从0开始的
# # #     print id,item
# # for id ,item in enumerate(tu,10):#可以在后面指定索引下标从10开始
# #     print id ,item

