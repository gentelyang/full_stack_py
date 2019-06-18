#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:gentelyang  time:2019-06-13

#1:time模块

#时间戳
import time
time.sleep(1)
time.time()#时间戳1560407744.72,从1970年到现在的时间秒数

#结构化时间
time.localtime()#time.struct_time(tm_year=2019, tm_mon=6, tm_mday=13, tm_hour=14, tm_min=38, tm_sec=16, tm_wday=3, tm_yday=164, tm_isdst=0)
t1=time.localtime()
#print t1.tm.years#可以通过它获取对应的时间
#print t1.tm_tm_wday

#字符串时间2019-06-13(format string),将结构化时间localtime转化为字符串时间
print time.strftime("%Y-%m-%d %X",time.localtime())#2019-06-13 14:49:46
print time.asctime()#Thu Jun 13 14:54:49 2019
print time.ctime()#Thu Jun 13 14:54:49 2019

#datetime模块，输出的时间是最精准的
import datetime
print datetime.datetime.now()#2019-06-13 14:57:16.353359

#random模块
#验证码时会用到随机数
import random
ret1 = random.random()#产生一个0-1的浮点数
print ret1#0.513506564728产生一个随机数
ret2 = random.randint(1,3)#可以取到3这个值
print ret2
ret3 = random.randrange(1,3)#取不到3这个值
print ret3
ret4 = random.choice([1,2,3,4])#对某个可迭代对象进行随机选取数列中的一个值
print ret4
ret5 = random.sample([1,2,3,4],2)#从迭代对象list列表中随机选取两个值
print ret5
ret6 = random.uniform(1,4)#对1-4的均值分布产生一个随机数
print ret6
list1 = [1,2,3,4,5]
ret7 = random.shuffle(list1)#ret7返回的是None，但是list1已经被打乱
print list1#[4, 5, 3, 2, 1],其中list1被打乱了

def v_code():
    ret8 = ""
    for i in range(4):
        num = random.randint(0,9)
        alf = chr(random.randint(65,91))#chr的字符串作用就是将数字64转化为小写字母a
        s = str(random.choice([num,alf]))#因为ret8为字符串，所以要将整型转化为字符串类型
        ret8 += s
    return ret8
print v_code()


#sys模块
import  sys
import os
print sys.path#会输出一个list列表，前一个是自己定一个的，后面的是洗头膏的
#['/Users/liyang109/PycharmProjects/py_full_stack/basis_python', '/Users/liyang109/PycharmProjects/py_full_stack', '/Users/liyang109/PycharmProjects/py_full_stack/venv/lib/python27.zip', '/Users/liyang109/PycharmProjects/py_full_stack/venv/lib/python2.7', '/Users/liyang109/PycharmProjects/py_full_stack/venv/lib/python2.7/plat-darwin', '/Users/liyang109/PycharmProjects/py_full_stack/venv/lib/python2.7/plat-mac', '/Users/liyang109/PycharmProjects/py_full_stack/venv/lib/python2.7/plat-mac/lib-scriptpackages', '/Users/liyang109/PycharmProjects/py_full_stack/venv/lib/python2.7/lib-tk', '/Users/liyang109/PycharmProjects/py_full_stack/venv/lib/python2.7/lib-old', '/Users/liyang109/PycharmProjects/py_full_stack/venv/lib/python2.7/lib-dynload', '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7', '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-darwin', '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-tk', '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-mac', '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-mac/lib-scriptpackages', '/Users/liyang109/PycharmProjects/py_full_stack/venv/lib/python2.7/site-packages']
sys.path.append(r"可以为绝对路径，但是将其写死不灵活")#这个是临时修改，不能永久修改模块的路径
#用下面的写法更灵活
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


#os模块
os.getcwd()#获取当前工作目录
os.chdir("test1")#改变当时的目录
os.getcwd()#当前目录就发生改变了
os.pardir()#获取当前目录的父目录字符串
os.makedirs("dirname/dirname1")#可生成多层的递归目录
os.removedirs("dirname1:")#若目录为空则删除，并递归到上一层
os.mkdir()#生成单级目录
os.rmdir()#删除单机空目录
os.listdir("dirnname")#liechu
os.removedirs()




