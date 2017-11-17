#!/usr/bin/env python
# coding = utf-8


import os
import sys
import re
import gzip
import xml.etree.cElementTree as ET

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
        self.title = []
        self.values = []
        self.buff=[]

    def readXML(self,xmlPath,csvfile):
        objectNum = 0
        toFile = open('write.csv' ,'w+')                                             #以追加的方式打开文件write.csv
        for event, elem in ET.iterparse(xmlPath, events=('end',)):             #注意这里只使用标签的 end事件 进行触发即可
            #self.line={}                                                         # 清空self.line

            if elem.tag == 'v':                     #v 标签处理
                if elem.text :                           #如果标签的text 存在
                    v = elem.text.strip().split(' ')
                    self.values.append(v)       #把elem的 text 属性 用 ' ' 分割为列表 然后把列表添加到 self.values列表 中
                    for i,value in  enumerate(v):        # 遍历self.values
                        self.line[self.title[i]] = v[i]   # 给字典self.line 赋值: key 为self.title[i] , 值为self.values[i]
                else:                                               #注意 self.values 为二元列表
                    print("Result is None!")        #如果标签的text 为空 则打印 "Result is None!"

            elif elem.tag == 'object':               #object 标签处理
                self.line.update(elem.attrib)          #把字典elem.attrib 合并到self.line中
                self.buff.append(dict(self.line))      # 把字典self.line 添加到 self.buff 列表中 list() 深拷贝list
                for key,value in self.line.items():
                    if not (key in self.title):                                     #如果self.title中不存在key 则添加key到title中
                        self.title.append(key)
                objectNum += 1
                self.line={}                                                         # 清空self.line

            elif elem.tag == 'smr' :                   #如果遇到 smr 标签结束
                if elem.text :                           #如果标签的text 存在
                    self.title = elem.text.split(' ')       #把elem的 text 属性 用 ' ' 分割为列表 存储在 self.title 中
                else:
                    print("Result is None!")        #如果标签的text 为空 则打印 "Result is None!"



            elem.clear()                            #清楚标签

            if objectNum == 10:                    #如果objectNum等于100,
                for tofileline in  self.buff:       #迭代self.buff,的每一项
                    tmp = list(map(lambda x: x + ',', tofileline))      #使用map函数 给tofileline列表的每一项都增加字符 ','
                    tmp[-1] = tmp[-1][:-1]                                # 是tofileline 列表的最后一项去掉最后一个字符 ','
                    toFile.writelines(tmp)        #写入tmp列表 到文件toFile中

                toFile.flush()                      #立即写入缓冲区文件
                self.buff.clear()                   #清空self.buff列表
                objectNum = 0                       #复位objectNum变量

        for tofileline in  self.buff:       #迭代self.buff,的每一项
            tmp = list(map(lambda x: x + ',', tofileline))      #使用map函数 给tofileline列表的每一项都增加字符 ','
            tmp[-1] = tmp[-1][:-1]                                # 是tofileline 列表的最后一项去掉最后一个字符 ','
            toFile.writelines(tmp)        #写入tmp列表 到文件toFile中

        #toFile.seek(0,0)                                        #将文件指针移动到文件第一行第一个字符,即将写入文件标题
        #if not (toFile.tell()):
        tmp = list(map(lambda x: x + ',', self.title))      #使用map函数 给self.title列表的每一项都增加字符 ','
        tmp[-1] = tmp[-1][:-1]                                # 是tofileline 列表的最后一项去掉最后一个字符 ','
        toFile.writelines(tmp)        #写入tmp列表 到文件toFile中,(将标题写入文件最后一行)

        print("Over!")
        toFile.close()                           #关闭文件
if __name__=="__main__":
    xml = ungzip(r'E:\工具\资料\宝鸡\研究\Python\python3\sshMR\mrdata\FDD-LTE_MRE_NSN_OMC_772566_20171106011500.xml.gz', r'E:\工具\资料\宝鸡\研究\Python\python3\sshMR\mrdata\FDD-LTE_MRE_NSN_OMC_772566_20171106011500.xml')
    readxml = readXMLET()
    readxml.readXML(r'E:\工具\资料\宝鸡\研究\Python\python3\sshMR\mrdata\FDD-LTE_MRE_NSN_OMC_772566_20171106011500.xml', r'E:\工具\资料\宝鸡\研究\Python\python3\sshMR\mrdata\FDD-LTE_MRE_NSN_OMC_772566_20171106011500.csv')


