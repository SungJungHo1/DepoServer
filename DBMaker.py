from pymongo import MongoClient
from Ordersdatas import *
from datetime import *
from random import *
from datetime import datetime, timedelta, timezone
import shortuuid
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
WaitTime = mydb['WaitTime']
Depo = mydb['Depo']

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
                if int(datess.seconds / 60) >= 30:
                    Order_Code = i["Order_Code"]
                    Update_deposit(Order_Code, False)
                    Update_Cancel(Order_Code, True)
                    push_Message(i['UserId'],'ขออภัยค่ะคุณลูกค้าหลังจาก 30 นาทีของการสั่งอาหาร รายการจะถูกยกเลิกอัตโนมัติเพราะลูกค้าโอนเงินล่าช้า กรุณาเลือกสั่งรายการอาหารใหม่อีกครั้งค่ะ🙏')
                    
        elif not i["Cancel"]:
            if "deposit" not in i:
                datetime_result = datetime.strptime(i['Order_Time'], form)
                dt_timezone = datetime_result.replace(tzinfo=timezone_kst)
                datess = datetime_utc2 - dt_timezone
                if int(datess.seconds / 60) >= 30:
                    Order_Code = i["Order_Code"]
                    Update_deposit(Order_Code, False)
                    Update_Cancel(Order_Code, True)
                    push_Message(i['UserId'],'ขออภัยค่ะคุณลูกค้าหลังจาก 30 นาทีของการสั่งอาหาร รายการจะถูกยกเลิกอัตโนมัติเพราะลูกค้าโอนเงินล่าช้า กรุณาเลือกสั่งรายการอาหารใหม่อีกครั้งค่ะ🙏')
                    

            elif not i["deposit"] :
                datetime_result = datetime.strptime(i['Order_Time'], form)
                dt_timezone = datetime_result.replace(tzinfo=timezone_kst)
                datess = datetime_utc2 - dt_timezone
                if int(datess.seconds / 60) >= 30:
                    Order_Code = i["Order_Code"]
                    Update_deposit(Order_Code, False)
                    Update_Cancel(Order_Code, True)
                    push_Message(i['UserId'],'ขออภัยค่ะคุณลูกค้าหลังจาก 30 นาทีของการสั่งอาหาร รายการจะถูกยกเลิกอัตโนมัติเพราะลูกค้าโอนเงินล่าช้า กรุณาเลือกสั่งรายการอาหารใหม่อีกครั้งค่ะ🙏')
                    

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

def Update_deposit(Order_Code, deposit):
    myquery = {"Order_Code": str(Order_Code)}
    newvalues = {"$set": {"deposit": deposit}}

    mycol.update_one(myquery, newvalues)

def Update_Cancel(Order_Code, Cancel):
    myquery = {"Order_Code": str(Order_Code)}
    newvalues = {"$set": {"Cancel": Cancel}}

    mycol.update_one(myquery, newvalues)

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
        if "Cancel" not in i:
            if "deposit" not in i:
                if int(T_Money) == int(money):
                    datetime_result = datetime.strptime(i['Order_Time'], format)
                    dt_timezone = datetime_result.replace(tzinfo=timezone_kst)
                    datess = datetime_utc2 - dt_timezone
                    if int(datess.seconds / 60) <= 30 and datess.days >= 0:
                        Order_Code = i["Order_Code"]
                        Update_deposit(Order_Code, True)
                        Update_Cancel(Order_Code, False)
                        Insert_Depo(UserId=i["UserId"],UserName=i["UserName"],Time=str_datetime,Money=money,Order_Code=i["Order_Code"],Finded=True)
                        return
        else:
            if not i["Cancel"]:
                if "deposit" not in i:
                    if int(T_Money) == int(money):
                        datetime_result = datetime.strptime(i['Order_Time'], format)
                        dt_timezone = datetime_result.replace(tzinfo=timezone_kst)
                        datess = datetime_utc2 - dt_timezone
                        if int(datess.seconds / 60) <= 30 and datess.days >= 0:
                            Order_Code = i["Order_Code"]
                            Update_deposit(Order_Code, True)
                            Update_Cancel(Order_Code, False)
                            Insert_Depo(UserId=i["UserId"],UserName=i["UserName"],Time=str_datetime,Money=money,Order_Code=i["Order_Code"],Finded=True)
                            return

                elif not i["deposit"] :
                    if int(T_Money) == int(money):
                        datetime_result = datetime.strptime(i['Order_Time'], format)
                        dt_timezone = datetime_result.replace(tzinfo=timezone_kst)
                        datess = datetime_utc2 - dt_timezone
                        if int(datess.seconds / 60) <= 30 and datess.days >= 0:
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

if __name__ == "__main__":
    ww = Depo.find({})
    for i in ww:
        print(i)
    # Add_cus_AddrData(5485851021533487,{'주소이름':'광주집','주소1':'월곡동','주소2':'빌라','좌표1':35.1673079492069,'좌표2':126.80982365415,})
    # www = WaitTime.find_one({"Time":'2022.12.15 21:25:33'})
    # www = WaitTime.find()
    # for i in www:
    #     print(i)
    # timezone_kst = timezone(timedelta(hours=9))
    # datetime_utc2 = datetime.now(timezone_kst)

    # format = '%Y-%m-%d'

    # str_datetime = datetime.strftime(datetime_utc2, format)
    # print(str_datetime)

    # timezone_kst = timezone(timedelta(hours=9))
    # datetime_utc2 = datetime.now(timezone_kst)
    # format = '%Y-%m-%d %H:%M:%S'

    # datetime_result = datetime.strptime("2022-12-18 17:48:00", format)
    # dt_timezone = datetime_result.replace(tzinfo=timezone_kst)

    # datess = dt_timezone - datetime_utc2
    # print(dt_timezone)
    # print(datetime_utc2)
    # print(datess)
    # print(type(datess.seconds))
    # print(type(datess.days))
    # str_datetime = datetime.strftime(datetime_utc2, format)


    # find_money('2022-12-17',17000)
    Find_All_Order()
    # print(www["message"])
    # tet = pattern.search(www["message"]).group()
    # print(tet.replace("- 매장명 : ",""))
    # Insert_Data("Uad859360a7e2589c8c213b3b47fc27a2",'크턱',orderdata,cart)
    # Drop_Users()
    # z = randrange(0,900)
    # Order_Code = str(datetime.now().hour) + str(datetime.now().month) + str(datetime.now().year) + str(datetime.now().day) + str(int(datetime.now().microsecond / 1000)) + str(z)[-1]
    # print('Order_Code')
    # x = errcol.find()
    # for i in x:
    #     print(i)
    # find_Order_Datas('Uad859360a7e2589c8c213b3b47fc27a2')
    # print(find_service())
    # Order_Code = shortuuid.uuid()
    # print(Order_Code)
    # print(type(Order_Code))
    # print(find_service())
    # Insert_cust("크턱", "010-6675-5961")
    # find_Allcust()
    # DB_Order_Data('LqVxBH5pAxpWvnJhYEfVR8')
    # print(find_Account())
    # Drop_Users()
    # Insert_Err("sdsdsdsdsds")
    # Edit_Data("1382022238380", "https://ibb.co/r22bKFs")