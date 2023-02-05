from pymongo import MongoClient
from Ordersdatas import *
from datetime import *
from random import *
from datetime import datetime, timedelta, timezone
import shortuuid
from Make_Datas import Wait_Time_Data,Shop_Link,Make_Base
import re

import requests
import json

pattern = re.compile("- 매장명 : \S+")

client = MongoClient('mongodb://fastfood:fastfood@43.200.202.12', 27017)

mydb = client['FastFoodDB']
mycol = mydb['OrderDatas']
mycustomer = mydb['Customer']
myAccount = mydb['Account']
errcol = mydb['Errors']
service = mydb['service']
Coupon_Data = mydb['Coupon_Data']
Remind_Data = mydb['Remind_Data']

WaitTime = mydb['WaitTime']
Depo = mydb['Depo']
def Find_Days_Remind_Data():
    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)
    format1 = '%Y-%m-%d'
    str_Days = datetime.strftime(datetime_utc2,format1)
    Data = Remind_Data.find_one({'일자':str_Days})
    if Data == None:
        return None,None,None
    else:
        return Data["일자"],Data["1일쿠폰"],Data["1주일 리마인드"]

def insert_Remind_Data(days,W_datas,M_datas):

    Remind_Data.insert_one({"일자":days,'1일쿠폰':W_datas,"1주일 리마인드":M_datas})

def find_7OverUser():
    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)
    format1 = '%Y-%m-%d'
    format2 = '%Y-%m-%d %H:%M:%S'

    v = mycustomer.find({})
    # for i in v:
    #     if i["UserId"] == 'Ua80cd1a19a12cb88657950e300a68594':
    #         print(i)
    W_Coupon_List = []
    for i in v:
        date_count = 0
        
        if i['Last_Order_Time'] != "" and len(i['Last_Order_Time']) == 19:
            # print(len(i['Last_Order_Time']))
            # print(i['Last_Order_Time'])
            datetime_result = datetime.strptime(i['Last_Order_Time'], format2)
            dt_timezone = datetime_result.replace(tzinfo=timezone_kst)
            datess = datetime_utc2 - dt_timezone
            date_count = datess.days
        
        elif i['Last_Order_Time'] != "" and len(i['Last_Order_Time']) == 10:
            datetime_result = datetime.strptime(i['Last_Order_Time'], format1)
            dt_timezone = datetime_result.replace(tzinfo=timezone_kst)
            datess = datetime_utc2 - dt_timezone
            date_count = datess.days

        if date_count > 7 and i["1W_Coupon"]:
            W_Coupon_List.append({'datas':i,'count':date_count})
    return W_Coupon_List
def Updata_CD(UserId,First_Coupon,W_Coupon,M_Coupon):
    mycustomer.update_one({"UserId": str(UserId)}, {
        '$set': {'First_Coupon': First_Coupon,'1W_Coupon': W_Coupon,'1M_Coupon': M_Coupon,}})
def insert_Coupon(UserId,First_Coupon,W_Coupon,M_Coupon,지급일자,쿠폰명):
    Coupon_Code = shortuuid.uuid()
    mycustomer.update_one({"UserId": str(UserId)}, {
        '$set': {'First_Coupon': First_Coupon,'1W_Coupon': W_Coupon,'1M_Coupon': M_Coupon,}})
    mycustomer.update_one({"UserId": str(UserId)},{ '$addToSet': { 'coupon_List': {'지급일자':지급일자,"쿠폰내용":쿠폰명,'쿠폰번호':str(Coupon_Code),"쿠폰보유":True}} })
    Insert_CouponTime(지급일자=지급일자,쿠폰내용=쿠폰명,쿠폰번호=str(Coupon_Code),유저아이디=str(UserId))

def Find_All():
    datas = []
    x = mycustomer.find()
    for i in x:
        datas.append(i)
    return datas

def Insert_CouponTime(지급일자,쿠폰내용,쿠폰번호,유저아이디):
    Coupon_Data.insert_one({"지급일자":지급일자,"쿠폰내용":쿠폰내용,'쿠폰번호':str(쿠폰번호),'소유자':유저아이디})

def Insert_WaitTime(Time,message):
    WaitTime.insert_one({"Time":Time,"message":message})

def Insert_Depo(UserId,UserName,Time,Money,Order_Code,Finded):
    Depo.insert_one({"UserId":UserId,'UserName':UserName,'Money':Money,"Order_Code":Order_Code,"Finded":Finded,"Time":Time})

def Find_All_Order():
    datas = []
    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)

    format = '%Y-%m-%d'
    str_datetime2 = datetime.strftime(datetime_utc2, format)

    x = mycol.find({"Order_Time": {"$regex": str_datetime2}}).sort("_id", -1)
    for i in x:
        form = '%Y-%m-%d %H:%M:%S'
        str_datetime = datetime.strftime(datetime_utc2, form)
        time_type = datetime.strptime(str_datetime,form)

        if "Cancel" not in i:
            if "deposit" not in i:
                datetime_result = datetime.strptime(i['Order_Time'], form)
                dt_timezone = datetime_result.replace(tzinfo=timezone_kst)
                datess = datetime_utc2 - dt_timezone
                if int(datess.seconds / 60) >= 20:
                    Order_Code = i["Order_Code"]
                    Update_deposit(Order_Code, False)
                    Update_Cancel(Order_Code, True)
                    if int(i['use_point']) > 0:
                        Edit_Point(i['UserId'], i['use_point'])
                        ments = Make_Base(i['UserId'], i['use_point'])
                        push_Message2(ments)
                    else:
                        ments = Make_Base(i['UserId'], 0)
                        push_Message2(ments)
                    
        elif not i["Cancel"]:
            if "deposit" not in i:
                datetime_result = datetime.strptime(i['Order_Time'], form)
                dt_timezone = datetime_result.replace(tzinfo=timezone_kst)
                datess = datetime_utc2 - dt_timezone
                if int(datess.seconds / 60) >= 20:
                    Order_Code = i["Order_Code"]
                    Update_deposit(Order_Code, False)
                    Update_Cancel(Order_Code, True)
                    if int(i['use_point']) > 0:
                        Edit_Point(i['UserId'], i['use_point'])
                        ments = Make_Base(i['UserId'], i['use_point'])
                        push_Message2(ments)
                    else:
                        ments = Make_Base(i['UserId'], 0)
                        push_Message2(ments)
                    

            elif not i["deposit"] :
                datetime_result = datetime.strptime(i['Order_Time'], form)
                dt_timezone = datetime_result.replace(tzinfo=timezone_kst)
                datess = datetime_utc2 - dt_timezone
                if int(datess.seconds / 60) >= 20:
                    Order_Code = i["Order_Code"]
                    Update_deposit(Order_Code, False)
                    Update_Cancel(Order_Code, True)
                    if int(i['use_point']) > 0:
                        Edit_Point(i['UserId'], i['use_point'])
                        ments = Make_Base(i['UserId'], i['use_point'])
                        push_Message2(ments)
                    else:
                        ments = Make_Base(i['UserId'], 0)
                        push_Message2(ments)
                    

        if "Wait_Time" in i:
            if "Order_End_Time" in i:
                OE_Time = datetime.strptime(i['Order_End_Time'],form)
                P_Time = OE_Time + timedelta(minutes=i['Wait_Time'])
                if (time_type > P_Time):
                    if 'Cancel' not in i:
                        if not i["Order_End"] and not i["Del_End"]:
                            Update_Db(i["Order_Code"], False, True,False)
                            push_Message(i['UserId'],'คุณลูกค้าคะได้รับอาหารหรือเครื่องดื่มยังคะหากได้รับแล้ว กรุณาถ่ายรูปส่งให้แอดมินหลังจากได้รับอาหารแล้วนะคะ🙏')
                    else:
                        if not i['Cancel']:
                            if not i["Order_End"] and not i["Del_End"]:
                                Update_Db(i["Order_Code"], False, True,False)
                                push_Message(i['UserId'],'คุณลูกค้าคะได้รับอาหารหรือเครื่องดื่มยังคะหากได้รับแล้ว กรุณาถ่ายรูปส่งให้แอดมินหลังจากได้รับอาหารแล้วนะคะ🙏')
    return datas

def push_Message2(datas):
    Line_tokens = f"Bearer Tk7BbAc9682XQuHWap8MIwUjKOqXV+aQ1a4XJWaSOnIBpbG1AT5dRtRnSTyeIjCJBdNolK8sDhEF5xbxK9ygvU0h8TiC1tgKHlGHGMSNoNB1lOBTkWs1aRqt54k26x1UEvig5LdK0iN+CClOO29z0AdB04t89/1O/w1cDnyilFU="
    header = {
        "Authorization": Line_tokens,
        "Content-Type": "application/json"
    }
    url = f"https://api.line.me/v2/bot/message/push"
    
    response = requests.post(url, headers=header, data=json.dumps(datas))
    print(response)

def Update_deposit(Order_Code, deposit):
    myquery = {"Order_Code": str(Order_Code)}
    newvalues = {"$set": {"deposit": deposit}}

    mycol.update_one(myquery, newvalues)

def Update_Cancel(Order_Code, Cancel):
    myquery = {"Order_Code": str(Order_Code)}
    newvalues = {"$set": {"Cancel": Cancel}}

    mycol.update_one(myquery, newvalues)

def Update_WTDb(Order_Code,Wait_Time):

    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)

    format = '%Y-%m-%d %H:%M:%S'
    str_datetime = datetime.strftime(datetime_utc2, format)

    myquery = {"Order_Code": str(Order_Code)}
    
    newvalues = {"$set": {"Order_End": False, "Del_End": False,"Wait_Time":Wait_Time,"Order_End_Time":str_datetime}}
    mycol.update_one(myquery, newvalues)
#waittime +20분
def find_WTime(date,time,MarketName):
    x = mycol.find({"Order_Time": {"$regex": date}}).sort("_id", -1)
    for i in x:
        if "Cart" in  i:
            if len(i["Cart"]) > 0:
                Market_Name = i["Cart"][0]['storeName']
                if Market_Name == MarketName:
                    if not i["Order_End"] and not i["Del_End"]:
                        if 'Cancel' in i:
                            if not i["Cancel"]:
                                if i["deposit"] :
                                    dd = Wait_Time_Data(i['UserId'],i['UserName'],int(time) + 20,Market_Name)
                                    Update_WTDb(i['Order_Code'],int(time) + 20)
                                    push_Message2(dd)
                                    return

def Edit_Point(UserId, point):
    mycustomer.update_one({"UserId": str(UserId)}, {
        '$inc': {'Point': int(point)}})

def find_Cansel(date,MarketName):
    x = mycol.find({"Order_Time": {"$regex": date}}).sort("_id", -1)
    for i in x:
        if "Cart" in  i:
            if len(i["Cart"]) > 0:
                Market_Name = i["Cart"][0]['storeName']
                if Market_Name == MarketName:
                    if not i["Order_End"] and not i["Del_End"]:
                        if 'Cancel' in i:
                            if not i["Cancel"]:
                                if i["deposit"] :
                                    Order_Code = i["Order_Code"]
                                    UserId = i['UserId']
                                    totalPrice = 0
                                    for v in i["Cart"]:
                                        totalPrice = totalPrice + int(v['totalPrice'])
                                    Back_Point = totalPrice + int(i['delivery_fee']) + int(i['Service_Money']) - int(i['Coupon_Pay'])
                                    dd = Shop_Link(UserId,Back_Point,Market_Name)
                                    Update_Db(Order_Code, True, False,False)
                                    Edit_Point(UserId, Back_Point)
                                    Update_deposit(Order_Code, False)
                                    Update_Cancel(Order_Code, True)
                                    push_Message2(dd)
                                    return
  

def find_money(date,money):
    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)
    format = '%Y-%m-%d %H:%M:%S'

    x = mycol.find({"Order_Time": {"$regex": date}}).sort("_id", -1)
    for i in x:
        totalPrice = 0
        for v in i["Cart"]:
            totalPrice = totalPrice + v['totalPrice']
        T_Money = totalPrice + int(i['delivery_fee']) + int(i['Service_Money'])
        str_datetime = datetime.strftime(datetime_utc2, format)
        Point = 0
        Coupon = i["Coupon_Pay"]
        if "use_point" in i:
            Point = i["use_point"]
        if "Cancel" not in i:
            if "deposit" not in i:
                if int(int(T_Money) - int(Point) - int(Coupon)) == int(money):
                    datetime_result = datetime.strptime(i['Order_Time'], format)
                    dt_timezone = datetime_result.replace(tzinfo=timezone_kst)
                    datess = datetime_utc2 - dt_timezone
                    if int(datess.seconds / 60) <= 20 and datess.days >= 0:
                        Order_Code = i["Order_Code"]
                        Update_deposit(Order_Code, True)
                        Update_Cancel(Order_Code, False)
                        Insert_Depo(UserId=i["UserId"],UserName=i["UserName"],Time=str_datetime,Money=money,Order_Code=i["Order_Code"],Finded=True)
                        return
        else:
            if not i["Cancel"]:
                if "deposit" not in i:
                    if int(int(T_Money) - int(Point)) == int(money):
                        datetime_result = datetime.strptime(i['Order_Time'], format)
                        dt_timezone = datetime_result.replace(tzinfo=timezone_kst)
                        datess = datetime_utc2 - dt_timezone
                        if int(datess.seconds / 60) <= 20 and datess.days >= 0:
                            Order_Code = i["Order_Code"]
                            Update_deposit(Order_Code, True)
                            Update_Cancel(Order_Code, False)
                            Insert_Depo(UserId=i["UserId"],UserName=i["UserName"],Time=str_datetime,Money=money,Order_Code=i["Order_Code"],Finded=True)
                            return

                elif not i["deposit"] :
                    if int(int(T_Money) - int(Point)) == int(money):
                        datetime_result = datetime.strptime(i['Order_Time'], format)
                        dt_timezone = datetime_result.replace(tzinfo=timezone_kst)
                        datess = datetime_utc2 - dt_timezone
                        if int(datess.seconds / 60) <= 20 and datess.days >= 0:
                            Order_Code = i["Order_Code"]
                            Update_deposit(Order_Code, True)
                            Update_Cancel(Order_Code, False)
                            Insert_Depo(UserId=i["UserId"],UserName=i["UserName"],Time=str_datetime,Money=money,Order_Code=i["Order_Code"],Finded=True)
                            return
    str_datetime = datetime.strftime(datetime_utc2, format)
    Insert_Depo(UserId="확인안됨",UserName="확인안됨",Time=str_datetime,Money=money,Order_Code="확인안됨",Finded=False)

def find_cust(UserId):

    DBs = mycustomer.find_one({"UserId": str(UserId), },{'_id': 0})

    return DBs

def find_Order_Datas(UserId):
    lis = []
    DBs = mycol.find({"UserId": str(UserId)},{'_id': 0}).sort("_id", -1)
    for i in DBs:
        lis.append(i)
        
    return {'Order_List':lis}

def DB_Order_Data(Order_Code):
    DBs = mycol.find_one({"Order_Code": str(Order_Code)},{'_id': 0})
    
    return DBs

def find_Allcust():

    DBs = mycustomer.find()
    return DBs


def Insert_service():

    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)

    format = '%Y-%m-%d %H:%M:%S'
    str_datetime = datetime.strftime(datetime_utc2, format)

    # service.insert_one({"Money": 3000,"ment":"วันนี้หยุดบริการ 1 วัน 🙏\nเปิดบริการอีกทีในวันพรุ่งนี้ค่ะ🙏\nขอบคุณที่ใช้บริการFASTFOODนะคะ","opened":False, "Time": str(str_datetime)})
    service.insert_one({"Money": 3000,"ment":"Test Ment","opened":False, "Time": str(str_datetime)})


def find_service():

    DBs = service.find().sort("_id", -1)

    return DBs[0]


def Insert_Err(Errors):
    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)

    format = '%Y-%m-%d %H:%M:%S'
    str_datetime = datetime.strftime(datetime_utc2, format)

    errcol.insert_one({"Errors": Errors, "Time": str(str_datetime)})


def Edit_Data(Order_Code, Ur):
    mycol.update_one({"Order_Code": str(Order_Code)}, {
        '$set': {'Addres_Url': str(Ur)}})

def Add_cus_AddrData(UserId, Ur):
    mycustomer.update_one({"UserId": str(UserId)}, { '$addToSet': { 'AddLists':  Ur} })


def Drop_Users():
    mycustomer.drop()

def Update_Db(Order_Code, Order_e, Del_e,Order_Time):

    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)

    format = '%Y-%m-%d %H:%M:%S'
    str_datetime = datetime.strftime(datetime_utc2, format)

    myquery = {"Order_Code": str(Order_Code)}
    
    if Order_Time:
        newvalues = {"$set": {"Order_End": Order_e, "Del_End": Del_e,"Order_End_Time":str_datetime}}
    else :
        newvalues = {"$set": {"Order_End": Order_e, "Del_End": Del_e}}
    mycol.update_one(myquery, newvalues)


def push_Message(UserId,text):
        Line_tokens = f"Bearer Tk7BbAc9682XQuHWap8MIwUjKOqXV+aQ1a4XJWaSOnIBpbG1AT5dRtRnSTyeIjCJBdNolK8sDhEF5xbxK9ygvU0h8TiC1tgKHlGHGMSNoNB1lOBTkWs1aRqt54k26x1UEvig5LdK0iN+CClOO29z0AdB04t89/1O/w1cDnyilFU="
        header = {
            "Authorization": Line_tokens,
            "Content-Type": "application/json"
        }
        url = f"https://api.line.me/v2/bot/message/push"
        datas = {"to": UserId,
                "messages": 
            [
                {
                'type': "text",
                'text': text,
                },
            ]}
        response = requests.post(url, headers=header, data=json.dumps(datas))

def Check_Days_Coupon():
    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)
    format1 = '%Y-%m-%d'
    format2 = '%Y-%m-%d %H:%M:%S'
    
    v = Find_All()
    W_Coupon_List = []
    W_Coupon_List2 = []
    for i in v:
        date_count = 0
        
        if i['Last_Order_Time'] != "" and len(i['Last_Order_Time']) == 19:
            # print(len(i['Last_Order_Time']))
            # print(i['Last_Order_Time'])
            datetime_result = datetime.strptime(i['Last_Order_Time'], format2)
            dt_timezone = datetime_result.replace(tzinfo=timezone_kst)
            datess = datetime_utc2 - dt_timezone
            date_count = datess.days
        
        elif i['Last_Order_Time'] != "" and len(i['Last_Order_Time']) == 10:
            datetime_result = datetime.strptime(i['Last_Order_Time'], format1)
            dt_timezone = datetime_result.replace(tzinfo=timezone_kst)
            datess = datetime_utc2 - dt_timezone
            date_count = datess.days

        if date_count >= 1 and date_count < 7 and i["1W_Coupon"]:
            W_Coupon_List.append(i)

        if date_count >= 7 and i["1M_Coupon"]:
            W_Coupon_List2.append(i)

    insert_Remind_Data(datetime.strftime(datetime_utc2,format1),W_Coupon_List,W_Coupon_List2)

if __name__ == "__main__":
    ww = Depo.find({})
    for i in ww:
        print(i)

    # x = WaitTime.find({})
    # for i in x:
    #     print(i)
    

    

    # v = mycustomer.find_one({'UserId':'Ua80cd1a19a12cb88657950e300a68594'})
    # print(v)
    # for i in v:
    #     if i["UserId"] == 'Ua80cd1a19a12cb88657950e300a68594':
    #         print(i)
    # finds = find_7OverUser()
    # insert_Coupon(UserId='Ua80cd1a19a12cb88657950e300a68594',First_Coupon=False,W_Coupon=True,M_Coupon=True,지급일자 = "2023-01-25",쿠폰명 = "첫주문 쿠폰")
    # Order_Time_Check(finds)



    # timezone_kst = timezone(timedelta(hours=9))
    # datetime_utc2 = datetime.now(timezone_kst)
    # format1 = '%Y-%m-%d'
    # format2 = '%Y-%m-%d %H:%M:%S'

    # v = Find_All()
    # W_Coupon_List = []
    # W_Coupon_List2 = []
    # for i in v:
    #     date_count = 0
        
    #     if i['Last_Order_Time'] != "" and len(i['Last_Order_Time']) == 19:
    #         # print(len(i['Last_Order_Time']))
    #         # print(i['Last_Order_Time'])
    #         datetime_result = datetime.strptime(i['Last_Order_Time'], format2)
    #         dt_timezone = datetime_result.replace(tzinfo=timezone_kst)
    #         datess = datetime_utc2 - dt_timezone
    #         date_count = datess.days
        
    #     elif i['Last_Order_Time'] != "" and len(i['Last_Order_Time']) == 10:
    #         datetime_result = datetime.strptime(i['Last_Order_Time'], format1)
    #         dt_timezone = datetime_result.replace(tzinfo=timezone_kst)
    #         datess = datetime_utc2 - dt_timezone
    #         date_count = datess.days

    #     if date_count >= 1 and date_count < 7 and i["1W_Coupon"]:
    #         W_Coupon_List.append(i)

    #     if date_count >= 7 and i["1M_Coupon"]:
    #         W_Coupon_List2.append(i)

    # insert_Remind_Data()
    # print(len(W_Coupon_List))
    # print(len(W_Coupon_List2))

    # Check_Days_Coupon()
    일자,주일,리마인드 = Find_Days_Remind_Data()
    print(주일)
    # xxx = Remind_Data.find({})
    # for i in xxx:

    #     print(i["일자"])