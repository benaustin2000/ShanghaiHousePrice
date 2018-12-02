# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 23:40:50 2018

@author: austin
"""

import requests
import re
from bs4 import BeautifulSoup,SoupStrainer
#import matplotlib.pyplot as plt

from fake_useragent import UserAgent
import time,random,sys
import pandas#pandas大法好

#ua=UserAgent()#使用随机header，模拟人类
#headers1={'User-Agent': 'ua.random'}#使用随机header，模拟人类
TotalPrice=[]  #Total price
InitialPrice=[]
UnitPrice=[]  #price per meter
HouseArea=[]
HouseHeight=[]
HouseConfig=[]
HouseCommunit=[]
HouseLocMajor=[]
HouseLocMinor=[]
HouseBuildYear=[]
HouseDealDate=[]
HouseDealCycle=[]
LinkUrl=[]

StrainerPriceInfo = SoupStrainer('a',attrs={'class':'nostyle'})
StrainerChengJiaoList = SoupStrainer('ul',attrs={'class':'listContent'})
StrainerTotalPage = SoupStrainer('div',attrs={'class':'page-box house-lst-page-box'})  #得到当前最大页数

PianQuList= ['北蔡', '碧云', '曹路', '川沙', '大团镇', '合庆', '高行', '高东', '花木', '航头', '惠南', '金桥', '金杨', '康桥', '陆家嘴', '老港镇', '临港新城', '联洋', '泥城镇', '南码头', '三林', '世博', '书院镇', '塘桥', '唐镇', '外高桥', '万祥镇', '潍坊', '宣桥', '新场', '御桥', '杨东', '源深', '洋泾', '张江', '祝桥', '周浦'] 
PianQuLink= ['/chengjiao/beicai/', '/chengjiao/biyun/', '/chengjiao/caolu/', '/chengjiao/chuansha/', '/chengjiao/datuanzhen/', '/chengjiao/geqing/', '/chengjiao/gaohang/', '/chengjiao/gaodong/', '/chengjiao/huamu/', '/chengjiao/hangtou/', '/chengjiao/huinan/', '/chengjiao/jinqiao/', '/chengjiao/jinyang/', '/chengjiao/kangqiao/', '/chengjiao/lujiazui/', '/chengjiao/laogangzhen/', '/chengjiao/lingangxincheng/', '/chengjiao/lianyang/', '/chengjiao/nichengzhen/', '/chengjiao/nanmatou/', '/chengjiao/sanlin/', '/chengjiao/shibo/', '/chengjiao/shuyuanzhen/', '/chengjiao/tangqiao/', '/chengjiao/tangzhen/', '/chengjiao/waigaoqiao/', '/chengjiao/wanxiangzhen/', '/chengjiao/weifang/', '/chengjiao/xuanqiao/', '/chengjiao/xinchang/', '/chengjiao/yuqiao1/', '/chengjiao/yangdong/', '/chengjiao/yuanshen/', '/chengjiao/yangjing/', '/chengjiao/zhangjiang/', '/chengjiao/zhuqiao/', '/chengjiao/zhoupu/']
#PianQuList=[]
#PianQuList.index('唐镇')   #24
#PianQuLink[PianQuList.index('唐镇')]   #'/chengjiao/tangzhen/'

MaxGetPage=100
TotalPage=MaxGetPage
HouseLocMajorString='浦东'

def SaveList():
    df=pandas.DataFrame({'总价':TotalPrice,'单价':UnitPrice,'房型':HouseConfig,'成交日期':HouseDealDate,
                         '成交周期':HouseDealCycle,'面积':HouseArea,'小区':HouseCommunit,'楼层':HouseHeight,
                         '区':HouseLocMajor,'板块':HouseLocMinor,'初始报价':InitialPrice,'楼龄':HouseBuildYear,
                         '网址':LinkUrl})
    datetimestr=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    df.to_csv(datetimestr+'-'+HouseLocMajorString+'-LianJia.csv')    

begin = time.time()
for PianQuGet in PianQuList:
    i=1
    RetryTimes=0
    PianQuNum=PianQuList.index(PianQuGet)
    while i<=TotalPage: # 100页最大值
        #http://sh.lianjia.com/chengjiao/tangzhen/pg1/
        domain = 'http://sh.lianjia.com'+PianQuLink[PianQuNum]+'pg'+str(i)
        headers1 = {'User-Agent': UserAgent().random, 'Accept-Language': 'zh-CN,zh;q=0.8'}#使用随机header，模拟人类
        sleeptime=random.randint(10, 20)/10
        time.sleep(sleeptime)
        res = requests.get(domain,headers=headers1)#爬取拼接域名
        #<ul class="listContent">
        PageNumHtml = BeautifulSoup(res.text,'html.parser',parse_only=StrainerTotalPage)
        # 把 string 变成 Dictionary
        if len (PageNumHtml) == 0: #遇到空页面
    #    PageNumDict = []
    #   if len(PageNumDict) == 0:   #25
            if RetryTimes>10:
                sys.exit("Error to get Page: "+domain)
            else:
                RetryTimes+=1
                sleeptime=random.randint(10, 20)/10+RetryTimes
                time.sleep(sleeptime)
                print('Retry after delay '+str(sleeptime)+' s :'+domain)
                continue
        RetryTimes=0
        PageNumDict = eval(PageNumHtml.div['page-data']) # {'totalPage': 25, 'curPage': 1}
        TotalPage = int(PageNumDict['totalPage']) 
        if TotalPage> MaxGetPage:
            TotalPage=MaxGetPage
        #更新抓取进度
        print('已经抓取'+PianQuGet+' 第'+str(i)+'/'+str(TotalPage)+'页 ''耗时: %.1f 分' %((time.time()-begin)/60))
        
        i+=1
        ChengJiaoListHtml=BeautifulSoup(res.text,'html.parser',parse_only=StrainerChengJiaoList)
        
        for ListItem in ChengJiaoListHtml.find_all('li'):
            #<div class="title"><a href="https://sh.lianjia.com/chengjiao/107100614568.html" target="_blank">创新佳苑 1室1厅 61.67平米</a></div>
    #        try:
            if ListItem.div.contents[1].find(class_='dealDate').string == '近30天内成交':
                continue
            else:
                HouseString=[]
                HouseString1=[]
                HouseString2=[]
                HouseString3=[]
                LinkUrl.append(ListItem.div.contents[0].a['href']) # https://sh.lianjia.com/chengjiao/107100614568.html
                HouseString = ListItem.div.contents[0].string.split()  #['金唐公寓', '2室2厅', '89.06平米']
                HouseArea.append(HouseString[2])
                HouseConfig.append(HouseString[1])
                HouseCommunit.append(HouseString[0])
                HouseString1=ListItem.div.contents[1].div.text.split('|') #'['南 ', ' 精装\xa0', ' 无电梯']
                HouseDealDate.append(ListItem.div.contents[1].find(class_='dealDate').string)  #'2018.10.24' or '近30天内成交'             
                TotalPrice.append(float(ListItem.div.contents[1].find(class_='number').string))   #386
                HouseString2=ListItem.div.contents[2].contents[0].text.split()     #'中楼层(共6层) 2006年建板楼'
                HouseHeight.append(HouseString2[0])
                HouseBuildYear.append(HouseString2[1])
                UnitPrice.append(int(ListItem.div.find(class_='unitPrice').span.string))   #unitPrice  43342
                #HouseString3 = ListItem.div.find(class_='dealCycleTxt').contents
                HouseLocMinor.append(PianQuList[PianQuNum])
                HouseLocMajor.append(HouseLocMajorString)
                
                HouseString=ListItem.div.find(text=re.compile('挂牌'))  # '挂牌391万'
                if (HouseString == None):
                    InitialPrice.append(' ')
                else:
                    InitialPrice.append(int(re.findall(r'\d+',HouseString)[0]))  
    
                HouseString=ListItem.div.find(text=re.compile('成交周期'))  # '成交周期119天'  ->119
                if (HouseString == None):
                    HouseDealCycle.append(' ')
                else:
                    HouseDealCycle.append(int(re.findall(r'\d+',HouseString)[0]))
    #        except:
    #           info=sys.exc_info()
    #           print(info[0],":",info[1])


SaveList()
    
#df=pandas.DataFrame({'总价':TotalPrice,'单价':UnitPrice,'房型':HouseConfig,'成交日期':HouseDealDate,
#                     '成交周期':HouseDealCycle,'面积':HouseArea,'小区':HouseCommunit,'楼层':HouseHeight,
#                     '区':HouseLocMajor,'板块':HouseLocMinor,'初始报价':InitialPrice,'楼龄':HouseBuildYear,
#                     '网址':LinkUrl})
#
#datetimestr=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
#df.to_csv(datetimestr+'-'+HouseLocMajorString+'-LianJia.csv')
