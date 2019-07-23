#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:gentelyang  time:2019-06-28
#接口
#继承同时具有两种含义
#1：继承基类的方法，并且做出自己的改变或者扩展
#2：声明某个子类兼容于某基类，定义一个接口类，子类继承接口类，并且实现接口中定义的方法
#接口继承要好于类继承，类继承已经将子类和父类耦合在一起了
#一切皆文件

# class All_file:
    # def read(self):
    #     pass
    # def write(self):
    #     pass
# class Disk(All_file):
#     pass

    # def read(self):
    #     print "disk read"
    # def write(self):
    #     print "disk write"

# class Cdrom(All_file):
#     pass
#
    # def read(self):
    #     print "Cdrom read"
    #
    # def write(self):
    #     print "Cdrom write"

import abc
class All_file():#接口类没有必要实例化
    @abc.abstractmethod
    def read(self):
        pass#接口类中方法没必要实现，只是一种规范,目的只是为了规范子类，它不用实现内部逻辑

    @abc.abstractmethod
    def write(self):
        pass

class Disk(All_file):
    def read(self):
        print "disk read"
    def write(self):
        print "disk write"

class Cdrom(All_file):
    def read(self):
        print "Cdrom read"

    def write(self):
        print "Cdrom write"

class Mem(All_file):
    def read(self):
        print "Mem read"
    def write(self):
        print "Mem write"

m1=Mem()
m1.read()
m1.write()
#归一化设置，接口继承的好处是每个继承All_file的接口都要实现All_file中的抽象方法
#只需要继续即可，不用管里面怎么实现，直接调用里面的基本的方法，只要兼容基类的接口即可
#python的类可以继承多个类，java和C#中则只能继承一个类
#python的类如果继承了多个类，那么其寻找方法有两种，分别为：深度优先和广度优先
