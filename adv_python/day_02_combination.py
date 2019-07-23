#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:gentelyang  time:2019-06-25
#组合
class Hand:
    pass

class Foot:
    pass

class Trunk:
    pass

class Head:
    pass


class Person:
    def __init__(self,id_num,name):
        self.id_num=id_num
        self.id_name=name
        self.hand=Hand()#
        self.foot=Foot()
        self.trunk=Trunk()
        self.head=Head()
p1=Person('111','alex')
print (p1.__dict__)

class School:
    def __init__(self,name,addr):
        self.name=name
        self.addr=addr

    def zhao_sheng(self):
        print "%s正在招生" %self.name

class Course:
    def __init__(self,name,price,period,school):
        self.name=name
        self.price=price
        self.period=period
        self.school=school

s1=School('Oldboy','北京')
s2=School('Oldboy','南京')
s3=School('Oldboy','东京')

msg='''
    1:oldboy北京校区
    2:oldboy南京校区
    3:oldboy东京校区
'''
while True:
    # print menu
    # print msg


    menu={

        1:s1,
        2:s2,
        3:s3
    }
    choice1=input('选择学校>>>:')
    school_obj=menu[choice1]
    # choice2=input('创建课程>>')

    name=input("课程名：>>")
    price=input("课程费用>>")
    period=input("课程周期>>")

    new_course=Course(name,price,period,school_obj)
    print "课程%s属于%s学校" %(new_course.name,new_course.school.name)


# c1=Course('linux','10','1h',s1)
# print c1.__dict__
# print c1.school
# print s1.name
