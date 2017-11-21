#!/usr/bin/env python
# coding = utf-8


import os
import sys
import re
import gzip
import xml.etree.cElementTree as ET
import pandas as pd

def ungzip(gzFile,xmlFile) :                                  #参数为.gz格式(未打包)的文件名
    xml = None                                          #返回值为:成功返回文件内容(文本),不成功返回None
    if os.path.exists(gzFile) :
        sfile = gzip.open(gzFile, mode='rb')
        xml = sfile.read()
        tfile = open(xmlFile, mode = 'w+', encoding = 'utf-8')
        tfile.write(xml.decode('utf-8'))
        sfile.close()
        tfile.close()
    return xml


class readXMLET():
    def __init__(self):
        self.line= {}
        self.lines = []
        self.title = []
        self.values = []
        self.buff=[]
        self.tablenames = []
        self.baseinfo = {}
        self.eNB_id = 0     #基站号
        self.mrType = ''    #mr文件类型 MRE MRO MRS

    def readXML(self,xmlPath,csvfile):
        objectNum = 0
        self.mrType = csvfile.split('_')[1]

        for event, elem in ET.iterparse(xmlPath, events=('start',)):             #注意这里只使用标签的 start事件 进行触发即可

            if elem.tag == 'fileHeader':               #measurement 标签处理
                self.baseinfo = dict(elem.attrib)           #保存MRS文件基础信息

            elif elem.tag == 'eNB':               #eNB 标签处理
                self.eNB_id  = elem.attrib['id']       #基站号
                break                            #结束循环
            elem.clear()                            #清楚标签

        for event, elem in ET.iterparse(xmlPath, events=('end',)):             #注意这里只使用标签的 end事件 进行触发即可
            #self.line={}                                                         # 清空self.line

            if elem.tag == 'v':                     #v 标签处理
                if elem.text :                           #如果标签的text 存在
                    v = elem.text.strip().split(' ')
                    self.values.append(v)       #把elem的 text 属性 用 ' ' 分割为列表 然后把列表添加到 self.values列表 中
                    for i,value in  enumerate(v):        # 遍历self.values
                        self.line[self.title[i]] = v[i]   # 给字典self.line 赋值: key 为self.title[i] , 值为self.values[i]
                    self.lines.append(dict(self.line))     #把self.line 的深拷贝添加到self.lines 中
                else:                                               #注意 self.values 为二元列表
                    print("Result is None!")        #如果标签的text 为空 则打印 "Result is None!"

            elif elem.tag == 'object':               #object 标签处理
                for self.line in self.lines :
                    self.line.update(elem.attrib)          #把字典elem.attrib 合并到self.line中
                    self.line.update(self.baseinfo)          #把字典self.baseinfo 合并到self.line中
                    self.buff.append(dict(self.line))      # 把字典self.line 添加到 self.buff 列表中 dict() 深拷贝self.line
                    for key,value in self.line.items():
                        if not (key in self.title):                                     #如果self.title中不存在key 则添加key到title中
                            self.title.append(key)
                objectNum += 1
                self.lines= []                                                      # 清空self.lines
                self.line= {}
                self.values = []
            elif elem.tag == 'smr' :                   #如果遇到 smr 标签结束
                if elem.text :                           #如果标签的text 存在
                    self.title = elem.text.split(' ')       #把elem的 text 属性 用 ' ' 分割为列表 存储在 self.title 中
                else:
                    print("Result is None!")        #如果标签的text 为空 则打印 "Result is None!"


            elif elem.tag == 'measurement':               #measurement 标签处理

                df = pd.DataFrame(self.buff)        #把self.buff 转化为 datafream 类型
                if not os.path.exists('.\\' + self.mrType + '\\' + self.eNB_id ) :
                    os.makedirs('.\\' + self.mrType + '\\' + self.eNB_id )
                if elem.attrib :
                    csvFullName = '.\\' + self.mrType + '\\' + self.eNB_id + '\\' + elem.attrib['mrName'] + os.path.basename(csvfile)
                else :
                    csvFullName = '.\\' + self.mrType + '\\' + self.eNB_id + '\\' + os.path.basename(csvfile)
                df.to_csv(csvFullName, mode = 'a+', index = False)     #保存为 csv文件 文件名为  measurement 标签 'mrName' 属性的值
                self.buff.clear()                   #清空self.buff列表
                self.title = []

            elem.clear()                            #清楚标签

        print("Over!")

if __name__=="__main__":
    xml = ungzip(r'E:\工具\资料\宝鸡\研究\Python\python3\sshMR\mrdata\FDD-LTE_MRS_NSN_OMC_772566_20171106011500.xml.gz', r'E:\工具\资料\宝鸡\研究\Python\python3\sshMR\mrdata\FDD-LTE_MRS_NSN_OMC_772566_20171106011500.xml')
    readxml = readXMLET()
    readxml.readXML(r'E:\工具\资料\宝鸡\研究\Python\python3\sshMR\mrdata\FDD-LTE_MRS_NSN_OMC_772566_20171106011500.xml', r'E:\工具\资料\宝鸡\研究\Python\python3\sshMR\mrdata\FDD-LTE_MRS_NSN_OMC_772566_20171106011500.csv')


