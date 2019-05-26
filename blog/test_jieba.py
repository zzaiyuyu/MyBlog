#-*- coding:utf-8 -*-
'''Zheng 's BUG'''
import sys
sys.path.append('../')
import jieba
import jieba.analyse
from optparse import OptionParser

topK = 10

content = "这么写代码的话，别扭不说，前端的那些构建工具比如webpack，gulp的使用范围也将大大降低。\
首先说结论，想完全剥离JS和模板而又需要使用模板渲染的数据，我是没想到什么好办法。如果读者有好办法希望赐教。\
既然不能完全剥离，那么就进最大的努力分离JS所需的数据和代码吧。\
既然需要模板渲染数据给JS使用，最先想到的办法就是把数据渲染到HTML代码中并隐藏。这种方法的优点就在于简单，甚至模板中都可以完全不使用<script></script>标签。缺点则是会渲染出很多的隐藏字段，JS中要写大量的getElementsByxxxx一类的代码来获取数据。\
既然如此，那么使用一种折中的办法，在HTML中使用<script></script>标签将后台传递的数据渲染成JS对象，然后JS代码中则可以直接使用这个对象了。"

tags = jieba.analyse.extract_tags(content, topK=topK, withWeight=True)
tags = dict(tags)
# for tag in tags:
    #print("tag: %s \t weight %f "%(tag[0], tag[1]))
print(tags)