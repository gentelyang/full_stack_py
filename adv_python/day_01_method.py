#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:gentelyang  time:2019-06-25
class Room:
    def __init__(self,name,owner,width,length):
        self.xingming=name
        self.zhuren=owner
        self.kuang=width
        self.chang=length
    @property
    def cal_area(self): #传的是一个self实例
        return self.kuang*self.chang

    @staticmethod#不能访问类属性也不能方法实例属性，它只是类的工具包
    def wash_body():#静态方法可以什么都不用传,传的参数不是实例参数也不是类参数
        print "洗刷刷；洗刷刷"


    def test(self):
        print "非静态方法，用类可以调用，但是实例无法调用"

    def test1(self):
        print "非静态方法，用类可以调用，但是实例无法调用"

    @classmethod
    def eat_food(cls):
        print "类方法传的时一个cls，而不是实例"

Room.cal_area#将cal_area当做类属性直接用，而不用在后面加()，Room.cal_area()
Room.wash_body()
#Room.test()#这个是报错的，类不能直接调用
r1=Room("wangfujing","ly","12","10")
r1.test()
r1.wash_body()