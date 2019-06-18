#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:gentelyang  time:2019-05-27

def func1(x,z,tpye="默认参数"):#x为形参,其中tpye为默认参数
    y = 2*x+3*z+1
    return y#返回值可以为null，可以为一个数，也可以为多个数以元组的形式给出
res1 = func1(2,3)#2,3实参，顺序不能乱
res2 = func1(z=3,x=2)#若指定z和x可以打乱顺序，默认参数默认可以不用传，如果要修改默认参数可以修改

print res1
print res2

def func2(x,*args,**kwargs):
#*args接收多个参数以列表的形式，**kwargs接收多个参数以字典的形式
    func2(1,2,3,4,a=1,b=2)
#其中1付给x，2，3，4以元组的形式传给*args;a=1,b=2以字典形式传给**kwargs



#匿名函数lambda
func3 = lambda x:x+1
print func3(10)
#匿名函数可以指定多个形参数
func4 = lambda x,y,z:x+y+z
print func4(1,2,3)#这样只能返回一个值
func5 = lambda x,y,z:(x+1,y+1,z+1)
print func5(1,2,3)#如果要返回多个值一定要加（），返回2，3，4


#map函数
# 1：普通方法实现
arr = [1,2,3,4]
def func6(arr):
    ret = []
    for i in arr:
        ret.append(i**2)
    return ret
#如上为普通函数的平方操作
# 2：使用自己构造的map函数实现
def func7(x):
    return x**2
def func8(x):
    return x-1
def map_func(func,arr):
    ret = []
    for i in arr:
        res = func(i)#这样就完全被写活了，可以传入任意的func()函数根据功能
        ret.append(res)
    return ret
print map_func(func7,arr)
print map_func(func8,arr)
# 3：使用系统内置函数map实现，功能如上相同
print map(lambda x:x+1,arr)#也可以和lambda联合使用，func可以为匿名函数
print map(func7,arr)
print map(func8,arr)
#最好将map结果输出为list,虽然map输出的结果默认是list,arr不一定为list，只要是可迭代对象就可以
print list(map(func7,arr))#将遍历的arr值交给func7去处理
print list(map(func8,arr))
#arr不一定必须为list列表，也可以是字符串，只要是可迭代对象就可以
str1 = 'liyang'
print list(map(lambda x:x.upper(),str1))#最后将str转化为list列表



#filter函数
# 1：同样先来一个普通函数实现filter功能，再学习内置filter函数
str2 = ['l_y','li','yang']
def filter_func(arr):
    ret = []
    for i in arr:
        if not i.startswith('l'):
            ret.append(i)
    return ret
print filter_func(str2)#将不是以l开头的字符串加入到ret，过滤掉了l_y 和li

#2：如下功能等价与前面等价
def func9(n):
    return n.startwith('l')
print filter(func9,str2)
# 3：结合匿名lambda函数一块使用
print filter(lambda x:x.startwith('y'))#与lambda结合使用



# reduce函数(在py2中可以直接用，但是在py3中被封装到了一个模块中）
from functools import reduce  #py3需要从functools中导入
# 1:普通方法实现求和操作,这种方法把逻辑写死了
arr1 = [1,2,3,4,5]
def add_func(arr):
    res = 0
    for num in arr:
        res += num
    return num
print add_func(arr1)

# 2：利用func做形参,不要将逻辑跑死
arr1 = [1,2,3,4,5]
def add_func1(func10,arr,init=None):#求乘积运算，init是否传初始值
    if init is None:
        res = arr.pop(0)#如果初始值为none，则pop出第一个1为初始值
    else:
        res = init
    for num in arr:
        res += func10(res,num)
    return res
print add_func1(lambda x,y:x*y,arr,100)

# 3：内置函数reduce
reduce(lambda x,y:x*y,arr,100)






#其它内置函数总结
print abs(-1)
print all([1,2,'1','2',''])#会将序列中每个元素非空是返回True，如果有一个为空为假返回False
print any([1,2,3,''])#只要有一个为真就是真，返回true
print bin(10)#将十进制转化为二进制
print bool('')#零、空和None为False，其它具体值都返回true
print bytes('ly',encoding='utf-8')#如果是中文'李洋'，需要编码一下。
#将一个字符串转化为字节的形式,输出的是二进制形式，就可以存入内存，在网络中传输
print bytes('李洋',encoding='utf-8').decode('utf-8')#用什么编码就需要用什么解码，防止乱码
#utf-8编码一个汉字三个字节，gbk编码一个汉字两个字节
print bytes('李洋',encoding='ascii')#ascii不能编码中文会报错，只能编码英文
print chr(97)#输出97对应的ascii码
print dir(all())#dir目录，打印某一个对象下面的方法，打印all内置函数中的所有方法
print divmod(10,3)#10除3取商和余数，返回(3,1）
print enumerate()

#eval功能
dic = {'name':'alex'}
dic_str = str(dic)#将dic转换为了字符串的形式"{'name':'alex'}"
print eval(dic_str)#将字符串中的内容提取出来
exp = '1+2*3'
print eval(exp)#eval计算exp表达式中的数学运算

#hash功能，可哈希内容即为不可变数据类型；不可hash的为可变数据类型
print hash('as123')#会输出一个hash值，无论传入的参数多长，hash输出的值是固定长度，不能根据结果进行反推
#print help(all())#help打印方法使用说明
print hex(10)#十进制转16进制
print oct(10)#十进制转8进制
print isinstance(1,int)#判断1是否是int的类型的实例对象

#min\max方法
arr2 = [1,2,3]
print min(arr2)
print max(arr2)

#zip用法
print zip(('a','b'),(1,2))#输出（'a',1),('b',2）是一一对应的作用
#如果不是一一对应的就会也不会报错
p = {'name':'ly','age':18}
print list(zip(p.keys(),p.values()))
#只要zip传入的是序列类型的就可以一一对应
print list(zip('hello','12345'))#输出[('h','1'),('e','2')....]

















        
























