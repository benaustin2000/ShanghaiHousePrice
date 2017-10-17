# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 21:35:15 2017

@author: austin
"""

#主要程序
import requests
import re
from bs4 import BeautifulSoup
import pandas#pandas大法好
from fake_useragent import UserAgent
import time,random,sys

ua=UserAgent()#使用随机header，模拟人类
headers1={'User-Agent': 'ua.random'}#使用随机header，模拟人类
TotalPrice=[]  #Total price
PricePerArea=[]  #price per meter
HouseArea=[]
HouseHeight=[]
HouseConfig=[]
HouseCommunit=[]
HouseLocMajor=[]
HouseLocMinor=[]
HouseBuildYear=[]
LinkUrl=[]
domain='http://sh.lianjia.com'#为了之后拼接子域名爬取详细信息
#res=requests.get('http://sh.lianjia.com/ershoufang/d1',headers=headers1)#爬取拼接域名
#time.sleep(random.randint(0.5, 1))
#soup = BeautifulSoup(res.text,'html.parser')#使用html筛选器

for i in range(1,100):#爬取2页，想爬多少页直接修改替换掉400，不要超过总页数就好
    begin = time.time()
    res=requests.get('http://sh.lianjia.com/ershoufang/d'+str(i),headers=headers1)#爬取拼接域名
    soup = BeautifulSoup(res.text,'html.parser')#使用html筛选器
     
    price=soup.find_all('span',attrs={'class':'total-price strong-num'})
    #price[0].string  # 323
    priceper=soup.find_all('span',attrs={'class':'info-col price-item minor'})
    #re.findall(r'\d{5}',priceper[0].string)  # ['66123']
    houseInfo=soup.find_all('span',attrs={'class':'info-col row1-text'})
    #houseInfo[0].get_text() #'\n\n\t\t\t\t\t\t\t1室1厅 | 40.53平\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t| 中区/5层\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t'
    #text=re.sub(r'\n\t*| |','',houseInfo[0].get_text()) #'1室1厅|40.53平|中区/5层'
    #re.split(r'\|', text) #['1室1厅', '40.53平', '中区/5层']
    houseAddr=soup.find_all('span',attrs={'class':'info-col row2-text'})
    #houseAddr2=houseAddr[0].find_all('a')
    #houseAddr2[0].string #'虹延小区'
    #houseAddr2[1].string #'长宁'
    #houseAddr2[2].string #'西郊'
    #re.findall(r'\d{4}',houseAddr[0].get_text()) # ['1995']
    #time.sleep(random.randint(0, 10)/10)
    j=0
    for j in range(0,29):
        try:
            LinkUrl.append(soup.select('.prop-title a')[j]['href'])
            TotalPrice.append(price[j].string)
            # 323
            UnitPrice=re.findall(r'\d{5}',priceper[j].string)
            #['66123']
            if UnitPrice:
                PricePerArea.append(int(UnitPrice[0])) # '66123'
            else:
                PricePerArea.append('unknow') # '1995'
            
            HouseInfo1=re.split(r'\|',re.sub(r'\n\t*| |平','',houseInfo[j].get_text()))
             #['1室1厅', '40.53平', '中区/5层']
            HouseArea.append(float(HouseInfo1[1]))
            HouseHeight.append(HouseInfo1[2])
            HouseConfig.append(HouseInfo1[0])
            
            houseAddr2=houseAddr[j].find_all('a')
            HouseCommunit.append(houseAddr2[0].string) #'虹延小区'
            HouseLocMajor.append(houseAddr2[1].string) #'长宁'
            HouseLocMinor.append(houseAddr2[2].string) #'西郊'
               
            BuildYear=re.findall(r'\d{4}',houseAddr[j].get_text())
            if BuildYear:
                HouseBuildYear.append(int(BuildYear[0])) # '1995'
            else:
                HouseBuildYear.append('unknow') # '1995'
        except:
           info=sys.exc_info()
           print(info[0],":",info[1])
    end = time.time()
    sleeptime=random.randint(5, 10)/10
    print(str(i),end - begin,sleeptime)       
    time.sleep(sleeptime)
    
df=pandas.DataFrame({'总价':TotalPrice,'单价':PricePerArea,'房型':HouseConfig,
                     '层':HouseHeight,'面积':HouseArea,'小区':HouseCommunit,
                     '区':HouseLocMajor,'板块':HouseLocMinor,'房龄':HouseBuildYear,
                     '网址':LinkUrl})

datetimestr=time.strftime('%Y-%m-%d',time.localtime(time.time()))
df.to_csv(datetimestr+'-LianJia.csv')
#def gethousedetail1(url,soup,j):#定义函数，目标获得子域名里的房屋详细信息
#    info={}#构造字典，作为之后的返回内容
#    s=soup.select('.info-col a')[1+3*j]#通过传入的j获取所在区的内容
#    pat='<a.*?>(.c)</a>'#构造提取正则
#    info['所在区']=''.join(list(re.compile(pat).findall(str(s))))#使用join将提取的列表转为字符串
#    s1=soup.select('.info-col a')[0+3*j]#[0].text.strip()
#    pat1='<span.*?>(.*?)</span>'
#    info['具体地点']=''.join(list(re.compile(pat1).findall(str(s1))))
#    s2=soup.select('.info-col a')[2+3*j]#[0].text.strip()
#    pat2='<a.*?>(.*?)</a>'
#    info['位置']=''.join(list(re.compile(pat2).findall(str(s2))))
#    q=requests.get(url)#使用子域名
#    soup=BeautifulSoup(q.text,'html.parser')#提取子域名内容,即页面详细信息
#    for dd in soup.select('.content li'):#提取class=content标签下的li标签房屋信息
#        a=dd.get_text(strip=True)#推荐的去空格方法，比strip（）好用
#    if '：' in a:#要有冒号的，用中文的冒号，因为网页中是中文  
#        key,value=a.split('：')#根据冒号切分出键和值
#        info[key]=value
#        info['总价']=soup.select('.bold')[0].text.strip()#提取总价信息
#    return info#传回这一个页面的详细信息

    

#for i in range(1,5):#爬取399页，想爬多少页直接修改替换掉400，不要超过总页数就好
#    res=requests.get('http://sh.lianjia.com/ershoufang/d'+str(i),headers=headers1)#爬取拼接域名
#    soup = BeautifulSoup(res.text,'html.parser')#使用html筛选器
##print(soup)
#for j in range(0,29):#网站每页呈现30条数据，循环爬取
#        url1=soup.select('.prop-title a')[j]['href']#选中class=prop-title下的a标签里的第j个元素的href子域名内容
#        url=domain+url1#构造子域名
#        print(soup)
#        houseary.append(gethousedetail1(url,soup,j))#传入自编函数需要的参数
#        


#df=pandas.DataFrame(houseary)
#df
#df.to_excel('house_lianjia.xlsx')