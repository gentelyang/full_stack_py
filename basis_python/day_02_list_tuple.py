#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:gentelyang  time:2019-05-22


#              list总结整理
#list特征
#list是一个类,通过list类创建对象，列表特征：用逗号分割每个元素，里面元素可以为任意类型。
list1 = [1,12,9,"name","age",[22,23,"瑞文"],True]
print len(list)


#取列表中元素
#可以存放任何类型的数据，下面时如何取数据
#1：根据索引取一个元素；2:根据切片去多个元素
l1 = list1[1]
l2 = list1[1:-1]
l3 = list[6][2]#取第六个元素列表中的瑞文

#循环
#循环取到所有的值
for item in list1:
    print item

#修改
#list创建后可以整理，内存中存储跟string不同，可以修改
list1[2]=22#替换，将第二个元素9替换为22
list1[3:5]=[120,119]#通过切片的方法替换

#删除
del list1[1]#del方法删除列表中特定值对应的元素
list1.pop()#pop方法默认将最后一个元素删除
list1.remove(1)#删除值为1的元素
#删除清空
list1.clear()#前面也不需要参数接收

#转换
#将字符串转换为list，先复习一下string转int，int转string
a = "123"
int(a)#将str转为int
b = 123
c=str(b)#将b转为字符串
l4 = list1("abc")#就可以将字符串转化为列表,内部使用for循环
#列表转字符串
# 1:(当列表中既有数字又有字符串时，需要通过for循环来实现)
s = ' '
for i in list1:
    s = s+ str(i)
print s
#2:(当列表中只有字符串时，可以通过.join()方法实现）
list2 = ["l","y"]
s = "".join(list2)

#添加
list1.append(5)#在后面追加,前面不需要写参数接收，l1=list1.append(5),结果时[,,,,,[5]]
list1.extend(5)#在后面追加5，结果时[,,,,5]
list1.insert("下标位置",6)#在下标位置插入6
print list1

#赋值拷贝
v1 = list1.copy()#浅拷贝，前面需要参数接收

#统计
v2 = list1.count(1)#统计list1中1出现的次数

#根据元素值查找元素的索引位置
v3 = list1.index(1)#查找1出现的索引位置

#排序
v4 = list1.sort()#list1对象调用了sort方法



##元组总结
#元组和列表类似，只是元组中的元素不能修改，不能增加或者删除
tup=(11,(2,3),3,4,5,6,)#一般元组的最后要加入一个逗号














