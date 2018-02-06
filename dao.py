import pymysql


db = pymysql.connect("localhost", "root", "root", "XiaoMai")

# 使用cursor()方法获取操作游标
cursor = db.cursor()


#将活动描述插入数据库
def insertDes(project,projectDes):
    id = None
    des = None

    length = len(project)
    index = 0
    sqlDes = "insert into description(performID,description)" \
             "VALUES (%s, %s)"
    print("准备插入数据------")
    db.set_charset('utf8')
    while index < length:
        id = project[index][0]

        print("这是ID:"+id)
        des = projectDes[index]
        print("这是描述:"+des)
        cursor.execute(sqlDes, (id,des.encode('utf-8')))
        db.commit()
        index+=1
    db.close()



#将活动信息插入数据库
def insertPro(projectID,name,time,venue,venueID,priceMin,projectType):
    oneID = None
    oneName = None
    oneTime = None
    oneVenue = None
    oneVenueID = None
    onePrice = None
    oneType = None

    sqlDes = "insert into perform(ID,name,time,address,addressID,priceMin,type)" \
             "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    db.set_charset('utf8')
    print("准备插入数据-------------")
    for index in range(0,len(projectID)):
        oneID = projectID[index][0]
        oneName = name[index]
        oneTime = time[index]
        oneVenue = venue[index]
        oneVenueID = venueID[index][0]
        onePrice = priceMin[index]
        oneType = str(projectType[index])
        print("这是ID:"+oneID)
        print("这是名称:"+oneName)
        print("这是时间:"+oneTime)
        print("这是地点:"+oneVenue)
        print("这是地点ID:"+oneVenueID)
        print("这是最低价格:"+onePrice)
        print("这是活动类型:"+oneType)
        cursor.execute(sqlDes,(oneID, oneName.encode('utf-8'), oneTime.encode('utf-8'),
                               oneVenue.encode('utf-8'), oneVenueID, onePrice.encode('utf-8'),
                               oneType))
        db.commit()

    db.close()

#将场馆信息插入数据库
def insertVenue(venueList):
    venueID = None
    venueName = None
    venueDes = None
    venueAddress = None

    sqlDes = "insert into venue(venueID, description, venue, location)" \
             "VALUES (%s, %s, %s, %s)"

    db.set_charset('utf8')
    print("准备插入数据---------")
    for oneVenue in venueList:
        venueID = oneVenue['ID']
        venueName = oneVenue['Name']
        venueDes = oneVenue['Des']
        venueAddress = oneVenue['Address']
        print("这是ID:"+venueID)
        print("这是名称:"+venueName)
        print("这是描述："+venueDes)
        print("这是地址:"+venueAddress)
        cursor.execute(sqlDes,(venueID, venueDes.encode('utf-8'), venueName.encode('utf-8'),
                               venueAddress.encode('utf-8')))
        db.commit()

    db.close()

#将价格信息插入数据库
def insertPrice(priceDic):
    oneID = None
    onePrice = None
    priceList = []
    index = None


    sqlDes = "insert into price(performID,priceOne,priceTwo,priceThree,priceFour,priceFive,priceSix)" \
             "VALUES (%s, %s, %s, %s, %s, %s, %s)"

    for oneProject in priceDic:
        oneID = oneProject['ID']
        onePrice = oneProject['Price']
        index = 0
        priceList = [] #每次进入先清空
        for count in range(0, 6):
            priceList.append(None)

        #暂时先取前6个价格
        for price in onePrice:
            priceList[index] = price
            index += 1
            if(index == 6):
                break


        cursor.execute(sqlDes,(oneID,priceList[0],priceList[1],priceList[2],priceList[3],
                               priceList[4],priceList[5]))
        db.commit()

    db.close()

projectID = [['10']]
name = ['望海国际']
time = ['2017.09.23-2018.03.02']
venue = ['人民大舞台']
venueID = [['53053']]
priceMin = ['80元起']
projectType = [1]


venue = [{'ID':'5423', 'Name':'贵阳星光', 'Des':'重庆市歌剧院', 'Address':'重庆长江一路62号地产大厦'}]
priceDic = [{'ID':'128788', 'Price':['80','150','180']}]
#insertPrice(priceDic)

#insertVenue(venue)
#insertPro(projectID,name,time,venue,venueID,priceMin,projectType)
