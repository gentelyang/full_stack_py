#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:gentelyang  time:2019-05-31
import os
os.getcwd()#获取当前.py文件的路径
#
# #f = open('file','rb',encoding='utf-8')#rb以字节形式读入，不需要后面加encoding编码
# f = open('file','rb')#这种方法是正确的写法，上面的不对
# #f1 = open('file','r',encoding='utf-8')#如果不加utf-8，系统默认是gbk形式编码，
# data = f.read()
# #"字符串----encode------》byte
# #byte-------decode------》『字符串』
# print data#读出的是字节形式,前面加了# -*- coding: utf-8 -*-就ok了
# print data.decode('utf-8')#和file文件中内容相同的输出形式
# f.close()
#
#
# #将str1转换为字节形式
# str1 = 'hello'
# #byte = bytes(str1,encoding='utf-8')#这里需要指定编码形式
#
# f2 = open('file','wb')#以byte形式写入,所以如果写入不是byte，需要bytes（）将其转为字节形式
# #f2.write(bytes('1111\n'),encoding='utf-8')#这里是一个字符串形式，所以需要将其转换为字节byte形式
# #f3 = open('file','ab')#追加到文本file的末尾
# #f3.write(bytes('李洋\n',encoding='utf-8'))

#当不知道源文件的编码时，需要读或者写的时候的方法
#f4 = open('file','r',encoding='latin-1')#用latin-1编码能尽可能多的显示需要显示的内容
#latin-1不能编码所以不好写入,可以在读的时候尽可能多的用
#data4 = f4.read()
#print data4
# f5 = open('file','w')
# f5.write('111\n''222\n''abc'.encode('utf-8'))#读入多个行的时候，中间不需要逗号，之间多个单引号就可以
# f5.flush()#将读入的111从内存中flush刷新到磁盘上；

# f6 = open('file','r')
# f6.readline()#每次只读取一行
# print f6.tell()#返回读后光标的位置
# print f6.readline()

f7 = open('file','rb')
# f7.readlines()#一次性将文件全部读出，并将其方法一个列表当中。此时会有\n这种转义字符，如果不想将转义字符打印出来可以使用read方法#
#一种常用的用于去除空行\n的方法，使用strip()
for i in f7.readlines():
  print i.strip('/n')#迭代输出并将\n给去除；

# print f7.readlines()
print
print f7.read()#read会原样的输出file文件中的内容，不会输出到list列表中；



