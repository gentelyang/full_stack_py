#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:gentelyang  time:2019-05-22

#字符串常规操作整理

# test="123456\t780"
#expandtabs()作用是从指定的位置断开,参数指定多少就在多少处断开，不够的空格填充。
test1="usernam\temail\tpassword\nliyang\tliyang109@baiu.com\t12345"
v1=test1.expandtabs(20)
v_1=test1.splitlines(True)#此时输出会保留\n (例如："password\n"）
v_2=test1.splitlines(False)#此时输出将会保留\n(例如："password")


test2 = " aLex"
t=' '
v2=test2.swapcase()#大小写转换
v3=test2.upper()#变大写，isupper()是判断是否为大写
v4=test2.lower()#lower将test2中的字符变为小写；islower是判断是否为小写
v5=test2.capitalize()#首字母改成大写
#v6=test2.caseflod()#所有的变小写，比lower更优秀一些
v7=test2.find("ex")#查找匹配串ex和源串匹配的第一个e对应的索引值
#v8=test2.isdecimal()#判断是否时数字#isdigit(),isnumeric()功能基本相同
v9=test2.isspace()#判断是否包含空格
v10=test2.istitle()#将普通字符转化为标题
v11=t.join(test2)#让test2中的每个字符按照t的形式进行拼接
v11_another=" ".join(test2)
v12=test2.center(20,"*")#对test2中内容设置长度为20，如果不够左右均匀用*补充
v13=test2.ljust(20,"*")#将test2的内容放到左边，右边如果不够20填充*
v14=test2.rjust(20,"*")
v15=test2.zfill(20)#指定宽度（长度）为20，当字符串len<20时，zfill用0进行填充
v16=test2.lstrip()#去除左边的空白
v17=test2.rstrip()#去除右边的空白
v18=test2.strip()#去除左右两边所有的空白,可去除/n /t
v19=test2.strip('a')#默认去除空白，可以指定去除的内容去除
v20=str.maketrans("abc",123)
v21=test2.translate(v20)#将test2中的abc替换为123
v20=test2.partition('L')#按照L进行划分,只能分割为3份，L一份，L之前一份，L之后一份
v21=test2.split('a',2)#按照字母a分割两次，分为了3份，但是a会消失拿不到
v22=test2.startswith('a')#判断是否以a开头
v23=test2.endswith('a')#判断是否以a结尾
v24=test2.swapcase()#大小写转换，小写变大写，大写变小写
v28=test2.replace("a","b")#将test2中的a替换为b
v29=test2.replace("a","b",2)#只将前两个a替换为b，后面的不进行替换


#format()的用法
test3="i am {name},age {age}"
test3.format(name="ly",age=26)
test3_easy="i am {0}, age {1}"
test3_easy.format("ly",26)
#test3.format_map("name":"ly","age":26)#依靠字典也可以

#获取字符串中的某一个字符
#1：通过索引下标获取某个字符
v25=test2[0]
#2:通过索引获取多个字符(切片)
v26=test2[1:3]
v27=test2[1:-1]

#此时输出的结果是竖着的一竖，遍历输出字符串的内容
index = 0
while index < len(test2):
    c=test2[index]
    print c
    index+=1


for item in test2:
    print item


#字符串创建后在内存不能修改，若修改会在内存中生成一个新的串
#会创建3块内存，有点费内存
name = "ly"
age = "18"
man = name + age

#range()方法占用内存相对较小，创建连续数字
for i in range(10):#等价于range(0,100)
    print i
#range()方法创建不连续的数字
for i in range(0,10,2):
    print i

#输出输入的内容及其对应的下标
test=input('>>>')
print test
print len(test)
for item2 in range(len(test)):
    print (item2,test[item2])



