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

#2:random模块
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


#3:sys模块
import  sys
import os
print sys.path#会输出一个list列表，前一个是自己定一个的，后面的是洗头膏的
#['/Users/liyang109/PycharmProjects/py_full_stack/basis_python', '/Users/liyang109/PycharmProjects/py_full_stack', '/Users/liyang109/PycharmProjects/py_full_stack/venv/lib/python27.zip', '/Users/liyang109/PycharmProjects/py_full_stack/venv/lib/python2.7', '/Users/liyang109/PycharmProjects/py_full_stack/venv/lib/python2.7/plat-darwin', '/Users/liyang109/PycharmProjects/py_full_stack/venv/lib/python2.7/plat-mac', '/Users/liyang109/PycharmProjects/py_full_stack/venv/lib/python2.7/plat-mac/lib-scriptpackages', '/Users/liyang109/PycharmProjects/py_full_stack/venv/lib/python2.7/lib-tk', '/Users/liyang109/PycharmProjects/py_full_stack/venv/lib/python2.7/lib-old', '/Users/liyang109/PycharmProjects/py_full_stack/venv/lib/python2.7/lib-dynload', '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7', '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-darwin', '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-tk', '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-mac', '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-mac/lib-scriptpackages', '/Users/liyang109/PycharmProjects/py_full_stack/venv/lib/python2.7/site-packages']
sys.path.append(r"可以为绝对路径，但是将其写死不灵活")#这个是临时修改，不能永久修改模块的路径
#用下面的写法更灵活
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import sys
print sys.argv
command =  sys.argv[1]
path =sys.argv[2]
import time
for i in range(10):
    sys.stdout.write('#')
    time.sleep(0.1)
    sys.stdout.flush()#正常的会将10个#放到缓存中，然后十个之后一块显示出
    #但是用了flush()后就是有一个返回一个，就想就像进度条一样了


#4:os模块
os.getcwd()#获取当前工作目录
os.chdir("test1")#改变当前脚本的工作目录，相当于shell下的cd
os.curdir()#返回当前目录（.）
os.pardir()#获取当前目录的父目录字符串
os.makedirs("dirname/dirname1")#可生成多层的递归目录
os.removedirs("dirname1:")#若目录为空则删除，并递归到上一层
os.mkdir()#生成单级目录
os.rmdir()#删除单机空目录
os.listdir()#列出指定目录下的所有文件和子目录,并以列表的形式打印
#若目录为空，则删除，并递归到上一层目录;如果要删除dirname2，要写成dirname1/dirnam2，然后返回到dirname1，如果dirname1为空，则dirname1也将被删除
os.removedirs('dirname1/dirname2')
os.rename('name1','name2')
os.stat('day_01_str.py')#获取文件目录信息
os.sep#输出os特定的路径分隔符，win下为\\,linux下为/
os.linesep#输出当前平台使用的终止符，win下为\t\r\n,linux下为\n
os.pathsep#输出分割文件路径的
os.system("bash command")#运行shell命令，直接显示
os.environ()#获取系统环境变量
os.path.abspath(path="")#返回path规划的绝对路径
os.path.split("path")#将path分割为目录和文件名二元组返回,例如home/gentelyang/day1.py会返回'home/gentelyang'和day1.py两个
os.path.dirname()#返回path的目录，其实是os.path.split(path)的第一个元素
os.path.basename()#返回path最后的文件名
os._exists("path")#如果path存在返回true，fouze
os.path.isfile("path")#如果path是一个存在的文件返回true
os.path.join("paht1","path2")#将两部分路径进行拼接，"path1/paht2/"
os.path.getatime(path)#返回path所指向的文件或者目录的最后存取时间
os.path.getmtime(path)#返回path所指向的文件或者目录的最后修改是时间

#5:json和pickle模块
#json将所有的数据类型都转化为了字符串str类型，#json只认双引不认单引
import json
dic = {'name':'alex'}
i = 8
s = 'hello'
list = [1,2,3]
data1 = json.dumps(dic)
date2 = json.dumps(i)
date3 = json.dumps(s)
data4 = json.dumps(list)
print data1 ,date2 ,date3 ,data4
print type(date2)#<type 'str'>
#{"name": "alex"} 8 "hello" [1, 2, 3]
data1 = json.dumps(dic)#data1将dic转化为str类型
f = open('file','w')
f.write(data1)
f_read = open("file",'r')
data = json.loads(f_read)#data1会被loads成为字典类型
print data#
print type(data)#这个输出的data是字典类型
#dump和dumps功能基本相同，只是用法稍有不同
json.dump(dic,f)#省略了很多步骤
with open("file",'r') as f:#file中的内容为一个字典{"name":"ly"}

    data5 = f.read()#拿到的是一个file文件中保存的一个str
    data6 = json.loads(data5)
    print data6["name"]#输出ly
    #并非只有dumps后的str才能loads，只要是字符串，都满足json规范，都能loads解析出来


#6:pickle和json基本上完全一样,只是pickle是二进制字节，而json是str
import pickle#
dic1 = {"name":'ly',"age":23}
f = open("序列化对象_pickle",'rb')
data = pickle.loads(f.read())#等价于pickle.load(f)
print data["age"]

#7:shelve模块
#shelve模块比pickle模块简单，只有一个open函数，返回类似字典的对象,key必须为str类型，val可为任何类型
import shelve
f = shelve.open(r'shelve.txt')

#8:xml模块
#通过如下方法遍历一颗xml树即可

import xml.etree.ElementTree as ET

tree = ET.parse("xmltest.xml")
root = tree.getroot()#<root>....</root>

print root.tag#返回根标签的名字
#遍历xml文档，解析xml树
for i in root:
    print i.tag#打印的是root标签下面的子标签
    print i.attrib#打印root标签下面country标签的属性，往往是键值对
    print i.text#<year>2019</year>2019就是text的内容，有些标签没有属性和text
    for j in i:
        print j.tag#打印的是root下面的子标签的子标签（root标签的孙子标签）
        print j.attrib#同样是打印属性
        print j.text

#xml的修改操作
for node in root.iter('year'):
    new_year = int(node.text)+1
    node.text = str(new_year)
    node.set("updated","yes")#增加一个属性updated=yes
tree.write("abc.xml")#将修改完的内容写入到abc.xml文件中
#xml删除node
for country in root.findall('country'):
    rank = int(country.find('rank').text)
    if rank > 50:
        root.remove(country)

#xml创建
new_xml = ET.Element("rootnode")
rootnode_child = ET.SubElement(new_xml,"child_node",attrib={"enrolled":"yes"})
rootnode_child_sex = ET.SubElement(rootnode_child,attrib={"en":"no"})


#9:re模块；针对字符串进行处理
#字符匹配，普通字符和元字符
#普通字符：大多数字符和自身
#元字符：. ^ $ * + ? {} [] | () \
import re
#   . 通配符
re.findall("a..x",'adsfaeyxssklg')
# ^开头
re.findall("^a..f",'adsfaeyxssklg')
#  $结尾
re.findall("s..g$",'adsfaeyxssklg')
