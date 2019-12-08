# -*- coding: utf-8 -*-

"""
在命令行中，用 buildozer init 生成 buildozer.spec， 修改某些参数后，运行
buildozer -v


"""


import kivy
kivy.require('1.10.0')  # replace with your current kivy version!

from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel

from kivy.properties import ListProperty
from kivy.lang import Builder
import kivy.resources

import re
import cProfile
from random import random
from kivy.config import Config


Config.set("graphics", "resizable", 0)
Config.set("graphics", "width", 430)
Config.set("graphics", "height", 270)


# Global variables 全局变量定义设置
## 可选输入框中的名称和选项列表，采用dict数据格式保存
lbl_name = {'长':[2],
            '宽':[60,80,100,150,200],
            '高':[40,60,80,100],
            '折边':[10,15,20],
            '密度':[7.85],
            '槽吨价':[5150,5200,5250,5350,5800,6150],
            '盖吨价':[5150,5200,5250,5350,5800,6150],
            '槽厚':[0.35,0.45,0.6,0.7,0.8,0.9,1.0,1.2],
            '盖厚':[0.35,0.45,0.6,0.7,0.8,0.9,1.0,1.2],
            '喷涂费':[0,5.5,6.5,9,10]
            }
lbl_cao = {'槽身成本价':[],
            '槽身销售价':[],
            '上浮率%':[0,5,6,7,8,9,10,11,12,13,14,15],
            '槽盖成本价':[],
            '槽盖销售价':[],
            '上浮率2%':[0,5,6,7,8,9,10,11,12,13,14,15],
            '每条成本价':[],
            '每条销售价':[],
            '毛利率%':[]
           }

lbl_pen = {'喷涂成本':[],
            '每条喷涂':[],
            '上浮率3%':[0,5,6,7,8,9,10,11,12,13,14,15],
            '每条喷涂线槽成本':[],
            '线槽销售价':[],
            '毛利率2':[]
          }

## 输入框常用长度设置
entry_len = 7
## 计算结果缺省长度设置
result_len =13
## 列数常数设置
ncolumn = 4
## 显示缺省公司名称设置
defaultCompany = '深圳市八达通线管桥架有限公司'
## 可选字体选项，用以区分关键结果显示和其他类型
defaultFont=[("Times New Roman",14),("Calibri",16),("Arial",18)]

# Builder.load_file("main.kv") same as Builder.load_string("""  """)

Builder.load_string("""
#:set zhfont1 'simfang.ttf'
###'uming.ttc'
#:set zhfont2 'simhei.ttf'
###'NotoSansCJK-Bold.ttc'

<Label>:
    font_size: 16
    font_name: zhfont1
    #size: 70, 70

<Button>:
    #size: 100, 60
    #pos: 0, 0
    color: 0,1,0,1  # RGB-Alpha
    font_size: 20
    font_name: zhfont1

<TabbedPanelItem>:
    font_name: zhfont2
    font_size: 16

<GridLayout>:
    spacing: 2   # [10,10] = [spacing_horizontal, spacing_vertical]
    size_hint: (0.9, 0.9)   # (1,1) full size of the parent
    pos_hint: {'center_x': .5, 'center_y': .5}

<RootWidget>:
    size_hint: 0.98, 0.98  # (1,1) full size of the parent
    pos_hint: {'center_x': .5, 'center_y': .5}
    do_default_tab: False
    
    TabbedPanelItem:
        text: '1.输入'
        GridLayout:
            id: _pgrid
            name: 'pgrid'
            cols: 4
            rows: 5
            background_color: (1, 1, 0, .5)  # 50% translucent red
            border: [0, 0, 0, 0]
            #background_image: 'path/to/background/image'
            
            Label:
                text: '长'
            FloatInput:
                id: _length
                text: '2'
                
            Label:
                text: '宽'
            FloatInput:
                id: _width
                text: '60'
                
            Label:
                text: '高'
            FloatInput:
                id: _height
                text: '40'

            Label:
                text: '折边'
            FloatInput:
                id: _zhebian
                text: '10'

            Label:
                text: '密度'
            FloatInput:
                id: _midu
                text: '7.85'

            Label:
                text: '槽吨价'
            FloatInput:
                id: _caodunjia
                text: '5150'

            Label:
                text: '盖吨价'
            FloatInput:
                id: _gaidunjia
                text: '5150'

            Label:
                text: '槽厚'
            FloatInput:
                id: _caohou
                text: '0.35'

            Label:
                text: '盖厚'
            FloatInput:
                id: _gaihou
                text: '0.35'

            Label:
                text: '    '
            Button:
                name: 'chengben_sale'
                text: '确定'
                id: btn_1
                on_release: root.chengben_sale()
                #on_press:
                #    root.current = root.ids['_sgrid']
                #    root.current = 'sgrid'
                    
                 
    TabbedPanelItem:
        text: '2.镀锌'
        GridLayout:
            id: _sgrid
            name: 'sgrid'
            cols: 6
            rows: 4
            
            Label:
                text: '槽身成本'
            TextInput:
                id: _caoshenjia

            Label:
                text: '槽身销售价'
            TextInput:
                id: _caoshensale
                
            Label:
                text: '上浮率%'
            FloatInput:
                id: _caoshenratio
                text: '11'

            Label:
                text: '槽盖成本'
            TextInput:
                id: _caogaijia

            Label:
                text: '槽盖销售价'
            TextInput:
                id: _caogaisale
                
            Label:
                text: '上浮率%'
            FloatInput:
                id: _caogairatio
                text: '11'

            Label:
                text: '每条成本价'
            TextInput:
                id: _hejichengben

            Label:
                text: '每条销售价'
            TextInput:
                id: _saleprice
                
            Label:
                text: '毛利率%'
            TextInput:
                id: _maolilv
                
            Button:
                name: 'duxin_sale'
                text: '确定'
                id: btn_2
                on_release: root.duxin_sale()

    TabbedPanelItem:
        text: '3.喷涂'
        GridLayout:
            id: _tgrid
            name: 'tgrid'
            cols: 6
            rows: 4
            spacing:10
            
            Label:
                text: '喷涂成本'
            TextInput:
                id: _pentucb

            #Label:
            #    text: '每条喷涂'
            #Label:
            #    text: '      '

            Label:
                text: '上浮率%'
            FloatInput:
                id: _penturatio
                text: '11'

            Label:
                text: '毛利率%'
            TextInput:
                id: _pentumaolilv

            Label:
                text: '喷线槽成本'
                # 每条喷涂线槽成本
            TextInput:
                id: _ptxccb

            Label:
                text: '喷线槽销售价'
            TextInput:
                id: _pentusale

            Label:
                text: '喷涂费'
            TextInput:
                id: _pentufei
                text: '5.5'
                

            Button:
                id: btn_3
                name: 'pentu_sale'
                text: '确定'
                on_release: root.pentu_sale()
""")


""" TestApp """

class RootWidget(TabbedPanel):
    def chengben_sale(self):
        "确定按钮，目的是获取参数值，计算槽身与槽盖成本价 "
        # 1. get parameters value
        p_length =  round(float(self.ids._length.text), 3)
        p_width =   round(float(self.ids._width.text), 3)
        p_height =  round(float(self.ids._height.text), 3)
        p_zhebian = round(float(self.ids._zhebian.text), 3)
        p_midu =    round(float(self.ids._midu.text), 3)
        p_caodunjia = round(float(self.ids._caodunjia.text), 3)
        p_gaidunjia = round(float(self.ids._gaidunjia.text), 3)
        p_caohou =  round(float(self.ids._caohou.text), 3)
        p_gaihou =  round(float(self.ids._gaihou.text), 3)
        #p_pentufei = round(float(self.ids._pentufei.text), 3)
        # self.ids._name.text equal seld.ids["_name"].text

        # 2. calculate chengbenjia
        __caoshenjia = (2 * (p_height + p_zhebian) + p_width)\
                      * p_length * p_caohou * p_caodunjia * p_midu / 1000000
        __caogaijia = (p_width + 2 * p_zhebian)\
                            * p_length * p_gaihou * p_gaidunjia * p_midu / 1000000
        __hejichengben = __caoshenjia + __caogaijia  #镀锌合计成本价格
       
        self.ids._caoshenjia.text = str(round(__caoshenjia, 2))
        self.ids._caogaijia.text = str(round(__caogaijia, 2))
        self.ids._hejichengben.text = str(round(__hejichengben, 2))

        # how to autolocate the second tab??? TODO
        # Test for printing all ids and values
        #for key, val in self.ids.items():
        #	print("key={0}, val={1}".format(key, val))

    def duxin_sale(self):
        # Frame2 中计算镀锌销售价格
        try:
            p_caoshenjia =  round(float(self.ids._caoshenjia.text), 3)
            p_caogaijia =   round(float(self.ids._caogaijia.text), 3)
            
            __csxsj = p_caoshenjia * (1+float(self.ids._caoshenratio.text)/100)
            __cgxsj = p_caogaijia  * (1+float(self.ids._caogairatio.text)/100)
            __hjxsj = __csxsj + __cgxsj   #镀锌合计销售价格
            __hjcbj = round(float(self.ids._hejichengben.text), 3)
            
            __dxmlv = (__hjxsj - __hjcbj) * 100 / __hjxsj  # 镀锌毛利率

            self.ids._caoshensale.text = str(round(__csxsj, 2))
            self.ids._caogaisale.text  = str(round(__cgxsj, 2))
            self.ids._saleprice.text   = str(round(__hjxsj, 2))
            self.ids._maolilv.text     = str(round(__dxmlv, 2))
            
        except ValueError as ve:
            #self.errinfo("错误信息", ve)
            print(ve)

    def pentu_sale(self):
        # Frame3 中计算喷涂成本价格
        try:
            p_length =  round(float(self.ids._length.text), 3)
            p_width =   round(float(self.ids._width.text), 3)
            p_height =  round(float(self.ids._height.text), 3)
            p_pentufei = round(float(self.ids._pentufei.text), 3)

            ##1 喷涂加工成本价格，有公式
            __pentucb = (p_height+p_width)*p_length*p_pentufei/250
            self.ids._pentucb.text = str(round(__pentucb, 2))
            
            ##2 每条喷涂线槽成本价格=喷涂成本+镀锌成本
            __hjcbj = round(float(self.ids._hejichengben.text), 3)
            __ptxccb = __hjcbj + __pentucb
            self.ids._ptxccb.text = str(round(__ptxccb, 2))
            
            ##3 Frame3 中计算每条喷涂线槽销售价格=喷涂线槽成本*（1+上浮率%）
            __ptxsj = __ptxccb * (1+float(self.ids._penturatio.text)/100)
            self.ids._pentusale.text = str(round(__ptxsj, 2))
            
            ##4 喷涂销售毛利率
            __ptmlv = (__ptxsj - __ptxccb) * 100 / __ptxsj
            self.ids._pentumaolilv.text = str(round(__ptmlv, 2))
            
        except ValueError as ve:
            print(ve)
            #self.errinfo("错误信息", ve)         


class FloatInput(TextInput):
    "only allow floats (0 - 9 and a single period)"
    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in\
substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)


# TestApp
class TestApp(App):
    def build(self):
        self.title = '线槽计算'  # defaultCompany
        return RootWidget()


if __name__ == '__main__':
    TestApp().run()
