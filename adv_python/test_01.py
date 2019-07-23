#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:gentelyang  time:2019-06-28
import pickle
#方法 一：

#
# class School:
#     def __init__(self,name,addr):
#         self.name=name
#         self.addr=addr
#
#     def save(self):
#         with open('file.db','wb') as f:
#             pickle.dump(self,f)
#
# class Course:
#     def __init__(self,name,price,period,school):
#         self.name=name
#         self.price=price
#         self.period=period
#         self.school=school
#
#
# #将信息永久的封存起来，然后利用pickle.load将其加载出来
# school_obj=pickle.load(open('file.db','rb'))
# print not school_obj.name,school_obj.addr
#方法 二：
class Base:
    def save(self):
        with open('file.db','wb') as f:
            pickle.dump(self,f)


class School(Base):
    def __init__(self,name,addr):
        self.name=name
        self.addr=addr


class Course(Base):
    def __init__(self,name,price,period,school):
        self.name=name
        self.price=price
        self.period=period
        self.school=school
