# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from bs4 import NavigableString
from urllib import request
import urllib3
import ssl
import re
import json
from collections import Counter
import dao



# 将url转化成html
def getHtml(url):
    try:
        req = request.Request(url)
        page = request.urlopen(req)
        html = page.read().decode('utf-8')

    except Exception as e:
        print("failed to geturl:", e)
        return ""
    else:
        return html

#得到所有的活动名称以及projectID
def getName(bsObj):
    count = 0
    for oneProject in bsObj.find_all('td', class_='name'):

        name.append(oneProject.string)
        print(oneProject.string)
        projectHtml.append(oneProject.a['href'])
        projectID.append(re.findall(
            r'//piao.damai.cn/(\d*).html', oneProject.a['href'], re.S
        ))
        count = count+1

        if(count == 500): #暂时取前500个
            break

    print(name)

#得到活动的描述
def getProjectDes(htmlList):
    print(htmlList)
    oneProDes = None
    strDes = None
    count = 0
    flag = False #判断有没有爬取到信息
    for oneHtml in htmlList:
        count = count+1
        miaoshu = ("这是第{}次 对应html：" + oneHtml).format(count)
        print(miaoshu)
        oneHtml = getHtml("https:"+oneHtml)
        bsProject = BeautifulSoup(oneHtml, 'html.parser')
        oneProDes = bsProject.find('div', class_='pre')

        flag = False
        if(oneProDes != None):
            for child in oneProDes.children:
                if(type(child) == NavigableString and child != '\n'):
                    projectDes.append(child)
                    flag = True
                    break
                elif(child.name == 'p' and child.string != None):
                    projectDes.append(child.string)
                    flag = True
                    break
        else:
            projectDes.append("暂时没有介绍")

        if(flag != True):
            projectDes.append("暂时没有介绍")

        print(projectDes)

#得到活动类型
def getProjectType(htmlList):
    onePro = None

    for oneHtml in htmlList:

        oneHtml = getHtml("https:"+oneHtml)
        print(oneHtml)
        bsProject = BeautifulSoup(oneHtml, 'html.parser')
        onePro = bsProject.find('p', class_='m-crm')
        for child in onePro.children:
            if(child.name == 'a'):
                if(child.string == "演唱会"):
                    projectType.append(1)
                elif(child.string == "音乐会"):
                    projectType.append(2)
                elif(child.string == "话剧歌剧"):
                    projectType.append(3)
    print(projectType)





#得到所有的活动时间
def getTime(bs):
    count = 0
    for oneProject in bs.find_all('td', class_='time'):
        time.append(oneProject.string)
        count = count+1
        if(count == 500): #暂时取500个
            break

    print(time)

#得到所有的最低价格
def getPriceMin(bs):
    count = 0
    for oneProject in bs.find_all('td', class_='price'):
        priceMin.append(oneProject.string)
        print(oneProject.string)
        count = count+1
        if(count == 500): #暂时取500个
            break

    print(priceMin)

#得到所有的活动地点以及场馆ID
def getVenue(bs):
    count = 0
    for oneProject in bs.find_all('td', class_='venue'):

        venue.append(oneProject.string)
        venueHtml.append(oneProject.a['href'])
        venueID.append(re.findall(
            r'//venue.damai.cn/venue_(\d*).html', oneProject.a['href'], re.S
        ))
        count = count+1
        if(count == 500): #暂时取500个
            break

    print(venue)
    #print(venueID)


# 得到地点的描述信息和地理位置
def getVenueDes(venueList):

    onlyList = list(set(venueList))

    oneVenueHtml = None
    oneVenueName = None
    oneVenueID = None
    oneVenueDes = None #描述
    oneVenueAdd = None #地址

    #print(Counter(onlyList))
    for oneVenue in onlyList:
        oneVenueDes = {}
        oneVenueID = re.findall(
            r'//venue.damai.cn/venue_(\d*).html', oneVenue, re.S
        )

        oneVenueHtml = getHtml('https:'+oneVenue)
        print(oneVenue)
        if(oneVenue == '//venue.damai.cn/venue_0.html'):
            continue
        bsVenue = BeautifulSoup(oneVenueHtml, 'html.parser')
        oneVenueName = bsVenue.find('input', id='ends')['value']
        oneVenueDes = bsVenue.find('div', id='agree').string
        if(oneVenueDes == None):
            oneVenueDes = '暂时没有介绍'
        oneVenueAdd = re.findall(
            r'场馆地址:(.*)', bsVenue.find('a', class_='VenueAddress').string, re.S
        )
        oneVenueDes = {'ID':oneVenueID[0], 'Name':oneVenueName, 'Des':oneVenueDes, 'Address':oneVenueAdd[0]}
        print(oneVenueDes)
        venueDes.append(oneVenueDes)
    print(venueDes)





#得到每个活动的价格表
def getPrice(totalList, list1):
    http = urllib3.PoolManager()
    urllib3.disable_warnings()
    priceDic = {}

    for oneProject in projectID:
        html_project = 'https://piao.damai.cn/ajax/getInfo.html?projectId={}'.format(int(oneProject[0]))
        print(html_project)
        r = http.request('GET', html_project)

        json_data = json.loads(r.data.decode('utf-8'))

        if(json_data['Data']['prices'] != None):
            for onePrice in json_data['Data']['prices']:
                    if(re.search(r'(\d+)', onePrice['PriceName'], re.S) != None):
                        list1.append(re.search(
                            r'(\d+)', onePrice['PriceName'], re.S
                        ).group(1))

        print(list1)
        priceDic = {'ID':oneProject[0], 'Price':list1}
        totalList.append(priceDic)#将一个活动的全部价格存入
        priceDic = {}
        list1 = []
        #print(totalList)
    print(totalList)






 #初始化
name = []
time = []
venue = []
venueHtml = []
venueID = []
venueDes = []

projectHtml = []
projectID = []
projectDes = []
projectType = []#活动类型 1代表演唱会 2代表音乐会 3代表话剧歌剧

priceMin = [] #用于首页显示的最低价格
priceRank = []  #存放每个活动的分区价格
price = [] #放全部活动的价格


DAMAI_URL = 'https://www.damai.cn/alltickets.html'
header = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
ssl._create_default_https_context = ssl._create_unverified_context
html = getHtml(DAMAI_URL)

bsObj = BeautifulSoup(html, 'html.parser')
getName(bsObj)
getProjectType(projectHtml)
getProjectDes(projectHtml)
dao.insertDes(projectID,projectDes)
getPrice(price,priceRank)
dao.insertPrice(price)
getTime(bsObj)
getPriceMin(bsObj)
getVenue(bsObj)
getVenueDes(venueHtml)
dao.insertVenue(venueDes)
dao.insertPro(projectID,name,time,venue,venueID,priceMin,projectType)



