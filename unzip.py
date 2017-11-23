#!/usr/bin/env python
# coding = utf-8


import os
import sys
import tarfile
import re
import gzip

reStr = r'Baoji-cell|Xian-cell|Xianyang-cell|Hanzhong-cell|Tongchuan-cell|Shangluo-cell|Yulin-cell|Yanan-cell|Weinan-cell|Ankang-cell'

#定义正则表达式 来匹配文件名
def isMatch(reStr, fileName):
    pattern = re.compile(reStr)
    match = pattern.match(fileName)
    return match

def unGz(fileName) :   # 解压缩gz文件 为经过Tar 打包的gz压缩文件
    #定义已解压的文件名
    unzipfiles = []
    if not os.path.exists(fileName) :
        #如果路径不存在 则打印'Path Is Not Exist!' 函数返回 -1
        print('File Does Not Exist!!!')
        return -1

    #替换文件路径中的'.' 为 '_",创建文件夹
    tagPath = fileName.replace('.', '_')
    if not os.path.exists(tagPath) :
        #如果路径tagPath不存在 则创建
        os.makedirs(tagPath)

    if tarfile.is_tarfile(fileName) : #判断文件是否tar 打包
        print('1')

    with open(fileName.replace('.gz', ''), 'r+') as tfile:
        with gzip.open(fileName, 'wb') as gfile:
            gfile.writelines(tfile)

    gfile.close()
    tfile.close()


def unTarGz(fileName, *reStr) :   # 解压缩文件 在压缩包 fileName 中,如果压缩包内的文件名匹配正则表达式 reStr 则解压缩此文件
    #定义已解压的文件名
    unzipfiles = []
    if not os.path.exists(fileName) :
        #如果路径不存在 则打印'Path Is Not Exist!' 函数返回 -1
        print('File Does Not Exist!!!')
        return -1

    #替换文件路径中的'.' 为 '_",创建文件夹
    tagPath = fileName.replace('.', '_')
    if not os.path.exists(tagPath) :
        #如果路径tagPath不存在 则创建
        os.makedirs(tagPath)

    #tarfile 打开压缩包文件
    tar = tarfile.open(fileName)
    #获取压缩包内的文件名保存到names
    names = tar.getnames()
    for name in names:
        #遍历文件名列表,如果 匹配正则表达式函数 isMatch() 则解压缩 文件到 tagPath 文件夹
        if isMatch(reStr,name):
            tar.extract(name, tagPath)
            unzipfiles.append(os.path.join(tagPath, name))
            print(os.path.join(tagPath, name) + 'unzip complate!')
    tar.close()
    return unzipfiles

if __name__ ==  '__main__' :
    unGz(r'E:\工具\资料\宝鸡\研究\Python\python3\sshMR\mrdata\FDD-LTE_MRE_NSN_OMC_772566_20171106011500.xml.gz')



