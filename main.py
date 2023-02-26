#!/usr/bin/env python
# coding: utf-8

# In[160]:


import pandas as pd
import os
import numpy as np
rootDir = r'./'


# In[207]:


# 循环目标路径下所有文件目录及名称
def getFiles():
    arr = []
    for filename in os.listdir('./'):
        if filename.endswith('.xlsx'):
            arr.append(filename)
    return arr


# In[208]:


# read excel
def readExcel(filename):
    path = os.path.join('./', filename)
    return pd.read_excel(path)


# In[209]:


# hande framedata
def handleFrameData(df):
    allData = {}
    allDataKeys = []
    counts = {}
    formatTime = "%Y/%d/%m/"
    duplicates = df.drop_duplicates(['日期','车牌'], keep='first')
    for idx, row in duplicates.iterrows():
        time = row['日期'].strftime(formatTime)
        row['日期'] = row['日期'].strftime(formatTime)
        key = time + row['车牌']
        allData[key] = np.array([])
        allDataKeys.append(key)
    dropedDf = df.drop(columns=['日期','单据编号','车牌'], axis = 1)
    for idx, row in df.iterrows(): ### 迭代数据 以键值对的形式 获取 每行的数据
        time = row['日期'].strftime(formatTime)
        row['日期'] = row['日期'].strftime(formatTime)
        key = time + row['车牌']
        if len(allData[key]) > 0:
            counts[key] += 1
            allData[key] = np.append(allData[key], dropedDf.values[idx])
        else:    
            allData[key] = np.append(allData[key], df.values[idx])
            counts[key] = 1
    
    return allData, counts

 
def mkdir(path):

    folder = os.path.exists(path)

    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径

    else:
        print("---  There is this folder!  ---")

def writeToExcel(df, filename):
    mkdir('./result')
    path = os.path.join('./result', filename)
    print('生成路径为：'+path)
    df.to_excel(path)

def createNewDf(allData, new_colums):
    arr = []
    max_items_num = 0
    for k, v in allData.items():
        newRow = np.array(v).flatten()
        arr.append(newRow.tolist())
    
    return pd.DataFrame(arr, columns=new_colums).fillna('')
    

def getColumns(df):
    return df.columns.values.tolist() ### 获取excel 表头 ，第一行

def getNewColumns(df, counts):
    new_colums = ['日期','单据编号','车牌',]
    base_columns = ['品名','单位','数量','单价','金额',]
    maxLen = 0
    for key, v in counts.items():
        if v > maxLen:
            maxLen = v

    for i in range(maxLen):
        for item in base_columns:
            new_colums.append(item + str(i+1))
    return new_colums


# In[212]:

if __name__ == '__main__':
    print('开始执行！！！！！！!')
    files = getFiles()
    for filename in files:
        print('正在处理文件：',filename)
        df = readExcel(filename)
        allData, counts = handleFrameData(df)
        new_columns = getNewColumns(df, counts)
        newDf = createNewDf(allData, new_columns)
        writeToExcel(newDf, filename)
        print('处理完成：',filename)
    print('成功！！！！！！！！！')
    
    


# In[ ]:




