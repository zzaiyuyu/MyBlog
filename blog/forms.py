#-*- coding:utf-8 -*-
'''Zheng 's BUG'''
from django import forms

# 一种是ModelForm 继承，一种是Form继承
class MusicForm(forms.Form):
    mid = forms.IntegerField(label="输入歌曲id")
    # 在python后台代码修改标签的html属性，是一个缺陷
    mid.widget.attrs['class'] = "form-control"
    page = forms.CharField()
    page.widget.attrs['class'] = "form-control"
    key = forms.CharField(label="关键字")
    key.widget.attrs['class'] = "form-control"
