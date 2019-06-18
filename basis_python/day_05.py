#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:gentelyang  time:2019-05-24

#字符串的百分号%
s1 = "li yang is a good " + "boy"#加号只能加到后面，加号会开辟新的内存空间
print s1
# s2 = 'li yang is a good %s ,age is %s' % 'boy' %18#这种方法是错误的，需要将所有的放在一个（）里前面加%
# print s2
#%s是万能的
s3 = 'li yang is a good %s ,age is %d' % ('boy',18) #%（第一个，第二个）
print s3

s4 = 'li yang is a good %s ,age is %s' % ('boy',[1,2])
print s4

#s5 = 'li yang is a good %s ,age is %d' % ('boy',[1,2])
#print s5#这个会报错，s5中的d%只能接受数字不能接受其它的，而s%可以接受一切，所以s4是对的

#浮点数,%.2f是小数后保留两位
s6 = "percent %.2f" % 99.97543
print s6

s7 = "i am %(pp).2f " %{"pp":12.345,}
print s7#通过字典的形式将12.35传给pp

# print ('root','x','0','0',sep=":")

#{:%}输出的是百分比的形式
s8 = "numbers:{:b},{:o},{:d},{:x},{:X},{:%}".format(12,12,12,12,12,12.54321)
print s8

