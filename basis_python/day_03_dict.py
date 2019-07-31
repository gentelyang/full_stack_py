#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:gentelyang  time:2019-05-23


#               字典
info = {
    "name":"ly",
    "age": 18,
    "k1":[11,22,33,{"kk1":"vv1","kk2":"vv2"}],
    "k2":(1,2,3,4),
    1:"abc",
    True:"123",#布尔值能作为key
   #[11,22]:"s",#列表不能作为key，但是元组可以作为key
   # {1:"a"}:"a"#字典也不能作为key
}

#字典是无序的

#查找字典中的值
#1:通过键的值找value值
v1 = info['name']
print v1
v2 = info["k1"][3]["kk1"]#查找vv1
#2:通过get方法取
v3 = info.get("k2")
#根据key获取值，当key不存在时返回后面参数的值
v4 = info.get("k5","没有k5时输出的内容或者数字")
print v4

#删除
del info["k1"]#删除这个键值对
del_val=info.pop("k1")#删除k1对应的val值


#循环
for item1 in info:#这个默认for循环输出的item是key
    print item1
for item2 in info.keys():#与上面item1等价,但本质无序，所以结果与上面不同
    print item2
for item3 in info.values():#只输出value
    print item3
for item4 in info:#输出key和value
    print (item4,info[item4])
for k ,val in info.items():#常用的输出key和value
    print (k ,val)


print "-------------------------"


#fromkeys方法
v5 = dict.fromkeys(["k","aaa",123])#会生成value为none的字典
print v5#{'k': None, 123: None, 'aaa': None}
v6 = dict.fromkeys(["k","aaa",123],123)#为key指定相同的123value值
print v6#{'k': 123, 123: 123, 'aaa': 123}

#setdefault()的功能，设置没有的值加入到字典中，如果存在不设置
v7 = info.setdefault("k4","123")

#update()的作用是更新
info.update({"原字典未有的值"："value值"})#此时相当于添加操作
info.update({"原字典中已经有的值":"需要改变的value值"})#此时相当于改变操作
dict1 = "{'haha":1,"hehe":2}
info.update(dict1)#此时是将dict1中的kye-value添加到info字典中




