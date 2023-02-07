# -*- coding: utf-8 -*-
from Get_yogiyo import *
from DBMaker import *
from Make_Datas import First_Order_Coup
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import time
import threading
from pydantic import BaseModel

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    date: str
    to: str
    message: str

def Send_1Day_Remind(일자,하루):
    for i in 하루:
        # print("진입1")
        time.sleep(5)
        insert_Coupon(i['UserId'],False,False,True,일자,'💗First Order Coupon💗')
        push_Message2(First_Order_Coup(i['UserId'],'อยากกินอาหารอะไรก็สั่งได้เลยนะคะต้อนรับสำหรับลูกค้าใหม่ให้คูปองค่าบริการฟรี 100%'))#첫주문 맨트
        

def Send_1W_Remind(일자,일주일):
    for i in 일주일:
        # print(일자)
        # print("진입2")
        push_Message2(First_Order_Coup(i['UserId'],'นาทีทองสำหรับลูกค้าวันนี้วันสุดท้ายของการใช้คูปองค่าบริการฟรี 100% เข้าไปเป็นเพื่อนสนิทกับ FASTFOOD ได้นะคะ'))#일주일 맨트
        Updata_CD(i['UserId'],False,False,False)
        time.sleep(5)

def Times():
    timezone_kst = timezone(timedelta(hours=9))
    
    days = 0

    DaySwich = False
    th_Swich = False
    

    while True:
        datetime_utc2 = datetime.now(timezone_kst)

        if days != datetime_utc2.day:    
            days = datetime_utc2.day
            DaySwich = False
            th_Swich = True
        hours = datetime_utc2.hour
        minutes = datetime_utc2.minute

        if int(hours) == 3 and int(minutes) >= 10 and not DaySwich:
            
            Check_Days_Coupon()
            DaySwich = True
            th_Swich = False
        
        if int(hours) >= 15 and int(minutes) >= 10 and not th_Swich:
            if Find_Days_Remind_Data() != None:
                th_Swich = True
                일자,하루,일주일 = Find_Days_Remind_Data()
                # print("진입")
                t1 = threading.Thread(target=Send_1Day_Remind, args=(일자,하루))
                t2 = threading.Thread(target=Send_1W_Remind , args= (일자,일주일))
                t1.daemon = True
                t2.daemon = True
                t1.start()
                t2.start()
            else:
                Check_Days_Coupon()
                DaySwich = True

        Find_All_Order()

        time.sleep(30)


@app.post('/wait-time')
def Waittime(item : Item):
    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)
    format = '%Y-%m-%d'
    str_datetime = datetime.strftime(datetime_utc2, format)
    Insert_WaitTime(item.date,item.message)
    if "주문 접수 안내" in item.message:
        pattern = re.compile("정상 접수되어, \d+")
        tet = pattern.search(item.message).group()
        xx = tet.replace('정상 접수되어, ',"")

        pattern2 = re.compile("매장명 : \S+")
        tet2 = pattern2.search(item.message).group()
        MarketName = tet2.replace('매장명 : ',"")
        find_WTime(str_datetime,int(xx),MarketName)

    if "익스프레스 주문 안내" in item.message:
        
        pattern = re.compile("주문이 \d+")
        tet = pattern.search(item.message).group()
        xx = tet.replace('주문이 ',"")

        # print(xx)

        pattern2 = re.compile("매장명 : \S+")
        tet2 = pattern2.search(item.message).group()
        MarketName = tet2.replace('매장명 : ',"")

        # print(MarketName)
        find_WTime(date = str_datetime,time = int(xx),MarketName = MarketName)
    
    if "취소" in item.message:

        pattern2 = re.compile("매장명 : \S+")
        tet2 = pattern2.search(item.message).group()
        MarketName = tet2.replace('매장명 : ',"")

        # print(MarketName)
        find_Cansel(date = str_datetime ,MarketName = MarketName)

    return item

@app.post('/wait-time_Push')
def Waittime_Push(item : Item):
    print(item)

    return item

@app.post('/depo')
def Depo(item : Item):
    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)
    format = '%Y-%m-%d'
    str_datetime = datetime.strftime(datetime_utc2, format)

    pattern = re.compile("입금\d+")
    if "네이버" not in item.message:
        tet = pattern.search(item.message.replace("원","").replace(",",""))
        if tet != None:
            money = tet.group().replace("입금","").replace(",","")
            Find_Depo(str_datetime, int(money))
    return item

@app.get('/Thread_Start')
def find_User_Data2(background_tasks: BackgroundTasks = None):
    background_tasks.add_task(Times)
    return "result"

if __name__ == "__main__":
    # text = f"126232321313\n입금100,000원\nsdsdsadasda"
    # if "네이버페이" in text:
    #     print("네이버페이")
    # pattern = re.compile("입금\S+")
    # tet = pattern.search(text.replace("원","")).group()
    # money = tet.replace("입금","").replace(",","")
    # print(money)
    # text = '요기요고객센터\n[주문 접수 안내]\n\n주문해주셔서 감사합니다.\n\n고객님의 소중한 주문이 정상 접수되어, 40분 내외로 도착 할 예정입니다.\n\n- 주문 일시 : 2023/01/04 19:54\n- 주문 번호 : F2301041953J99A8\n- 매장명 : 꼬치상회-월곡점\n- 주문 내역 : I.V 프로틴 흑당 밀크티 x 1 외 1 건\n- 배달 주소 : 경기도 이천시 중리동 (중\n'
    # text2 = '요기요고객센터\n[익스프레스 주문 안내]\n\n고객님의 주문이 14분 내외로 도착할 예정입니다.\n\n요기요 익스프레스가 빠르고 정확하게 배달해드릴게요.\n\n-  주문 일시 : 2023/01/02 15:26\n-  도착 예정 : 2023/01/02 15:43\n-  주문 번호 : F2301021526JZEA8\n-  매장명 : 용천통닭-월곡점\n-  주문 내역 : 통두마리 x 1\n-  배\n'

    # text3 = '[Web발신]\n[주문 전달 실패]\r\n\r\n소중한 식사 시간에 불편을 드려 죄송합니다.\r\n매장과의 연동 오류로 고객님의 주문이 음식점으로 전달되지 못했습니다.\r\n다른 음식점으로 주문을 부탁드립니다.\r\n\r\n- 주문 일시 : 2023/01/26 17:41\r\n- 주문 번호 : F2301261741J1YA8\r\n- 취소 사유 : 주문 전달 실패 (매장 연동 오류)\r\n- 매장명 : 롯데리아-인천불로점\r\n- 메뉴 : NEW홈투게더팩（사이다） x 1 외 1 건\r\n- 취소 금액 : 28,700원\r\n\r\n※ 24시 이후 취소 환불은 카드사 및 결제 수단에 따라 약 2~4일 정도 소요될 수 있습니다.\r\n(단, 주말, 공휴일 제외)\r\n\r\n서비스 이용에 불편을 드려 대단히 죄송합니다.'
    text4 = '[Web발신]\n하나,02/04,15:58\n23213213*****32321321\n입금15,000원\n맥도날드환불\n잔액80,090'
    # if "취소" in text3:

    #     pattern2 = re.compile("매장명 : \S+")
    #     tet2 = pattern2.search(text3).group()
    #     MarketName = tet2.replace('매장명 : ',"")

    #     print(MarketName)

    pattern = re.compile("입금\d+")
    tet = pattern.search(text4.replace("원","").replace(",",""))
    if tet != None:
        money = tet.group().replace("입금","").replace(",","")
        print(money)