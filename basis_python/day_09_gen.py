#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:gentelyang  time:2019-06-06

#生成器
#1：for循环生成
g_l = (i for i in range(10))

#2：生成器函数;yield结合next方法一块用，py2中是.next()方法；py3中是.__next__()方法
def test():
    yield 1
    yield 2
    yield 3#1：yield作用相当于return；2：yield可以保留上次函数运行的状态
    yield 4#利用yield生成多次，因为普通的函数只能生成一次；


res1 = test()
print res1.next()
print res1.next()
print res1.next()
print res1.next()#每次next都是基于上一个迭代结果向下的
#运行结果输出1，2，3，4

def product_baozi():

    for i in range(100):
        yield '包子%s' %i


baozi = product_baozi()
print baozi

baozi_1 = baozi.next()
baozi_2 = baozi.next()
print baozi_1
print baozi_2

#列表解析器
print sum([i for i in range(10)])
#生成器表达式
print sum(i for i in range(10))

def get_population():
    with open('dict_file','r') as f:
        for i in f:
            yield i
g = get_population()
#如果要输出字典类型的格式输出
dict_file = eval(g)
print dict_file
print dict_file['population']






