#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:gentelyang  time:2019-06-28

#继承
class Dad:
    money=10
    def __init__(self,name):
        print "baba"
        self.name=name

    def hit_son(self):
        print " %s 正在打儿子" %self.name


class Son(Dad):

    money = 1000
    def __init__(self,name,age):
        self.name=name
        self.age=age


print Son.money#继承了爸爸的10块钱
# Son.hit_son()
# print Dad.__dict__
# print Son.__dict__
s1=Son('alex',18)#创建实例会触发一个init，而Son中没有，所以会触发父类的init,所以需要传一个参数name

print s1.name
print s1.money
print Dad.money
print s1.__dict__#输出：name:alex






