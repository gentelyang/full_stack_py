#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:gentelyang  time:2019-06-06

#装饰器
#装饰器本质就是函数，为其它函数添加附加功能
#装饰器需要保证两个原则：1：不修改被修饰函数的源代码；2：不修改被修改函数的调用方式

#小的技巧，与装饰器无关
# l = [10,3,1,2,3,4,5]
# a.*_.c=l
# 其中a=10，c=5，_=中间的值
# a.*d.c=l
# a=10，c=5，d等于

#如下cal()函数是一个统计时间的函数
import time
def cal(l):
    start_time = time.time()
    res = 0
    for i in l:
        time.sleep(0.1)
        res += i
    stop_time = time.time()
    print "函数的运行时间是%s" %(stop_time-start_time)
    return res
print cal(range(10))
#如果还有其它函数需要加入时间统计的特性,如下函数都需要统计时间，不可能将cal（）函数
#的逻辑代码加入到如下函数中，那样会比较费事费力；
#如果你写的函数已经是在线运行的，那么函数要求加新功能，一行一行加逻辑，违反了开房封闭原则，不能修改源代码
#这样会影响别人的调用
def index():
    pass

def home():
    pass





#装饰器的知识储备
#装饰器=高阶函数+函数嵌套+闭包
#如下是一个非常容易懂的装饰器模式实例
def timemer(func):
    def wrapper(*args,**kwargs):
        start_time = time.time()
        res = func(*args,**kwargs)
        stop_time = time.time()
        print "函数运行时间是%s" %(stop_time-start_time)
        return res
    return wrapper

def cal_dec(l):
    res = 0
    for i in l:
        time.sleep(0.1)
        res += i
    return res

res = cal_dec(range(10))
print res




#高阶函数使用
#定义：1：函数接受的参数是一个函数名；2：函数的返回值是一个函数；满足其中任意一条就是高阶函数

def foo():
    print "你好py"

def test(func):
    start_time = time.time()
    print func
    stop_time = time.time()
    print "函数的运行时间%s" %(stop_time-start_time)

test(foo)#这就是一个高阶函数，传的参数为一个函数

#函数嵌套
#嵌套函数的内函数无这个参数时会向最近的外层函数去寻找这个参数
def father(name):
    def son():
        name="ll"
        print "儿子是%s" %name#此时的name传的时ll
    son()

def father(name):
    def son():
        print "儿子是%s" %name
        #当嵌套的内函数没有name这个参数时会往上找到father(name)这个参数传过去

    son()




#装饰器实现具体实例（重点掌握）
import time
def timer(func):
    def wrapper():
        start_time=time.time()
        func()
        end_time=time.time()
        print "运行时间时%s" (end_time-start_time)
    return wrapper#这个地方返回的是内函数
@timer#这个@timer就相当于下面的timer(test)
def test():
    time.sleep(3)
    print "test函数运行完毕"

res=timer(test)#返回的时wrapper的地址
res()#执行的是wrapper()
#下面的res就是在test函数上加了一个timer的装饰器，但是这样写比较费事，如果要给test
#函数加多个装饰器，那就会有多个这样的函数所以只需要利用@即可


#带参数验证功能的装饰器实例（重点掌握）
import time
user_list=[
           {"name":"ly","passwd":123},
           {"name":"tt","passwd":234},
           {"name":"hj","passwd":345}
]
current_dic={"username":None,"login":False}
def auth_func(func):
    def wrapper(*args,**kwargs):
        if current_dic['username'] and current_dic['login']:
            res=func(*args,**kwargs)
            return res
        username=input("用户名：").strip()
        passwd=input("密码：").strip()
        for user_dict in user_list:
            if username==user_dict["name"] and passwd==user_dict["passwd"]:
                current_dic["username"]=username
                current_dic["login"]=True
                res=func(*args,**kwargs)
                return res
        else:
            print "用户名或者密码错误"
    return wrapper

@auth_func
def index():
    print "欢迎来到京东』"

@auth_func
def home():
    print "终于回家了"


@auth_func
def work():
    print "i am coming"


















