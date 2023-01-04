from Get_yogiyo import *
from DBMaker import *
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import time
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

def Times():
    while True:
        time.sleep(30)
        Find_All_Order()

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

@app.post('/depo')
def Depo(item : Item):
    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)
    format = '%Y-%m-%d'
    str_datetime = datetime.strftime(datetime_utc2, format)

    pattern = re.compile("입금\S+")
    if "네이버" not in item.message:
        tet = pattern.search(item.message.replace("원","")).group()
        money = tet.replace("입금","").replace(",","")
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
    text = '요기요고객센터\n[주문 접수 안내]\n\n주문해주셔서 감사합니다.\n\n고객님의 소중한 주문이 정상 접수되어, 40분 내외로 도착 할 예정입니다.\n\n- 주문 일시 : 2023/01/04 19:54\n- 주문 번호 : F2301041953J99A8\n- 매장명 : 디저트39-이천점\n- 주문 내역 : I.V 프로틴 흑당 밀크티 x 1 외 1 건\n- 배달 주소 : 경기도 이천시 중리동 (중\n'
    text2 = '요기요고객센터\n[익스프레스 주문 안내]\n\n고객님의 주문이 14분 내외로 도착할 예정입니다.\n\n요기요 익스프레스가 빠르고 정확하게 배달해드릴게요.\n\n-  주문 일시 : 2023/01/02 15:26\n-  도착 예정 : 2023/01/02 15:43\n-  주문 번호 : F2301021526JZEA8\n-  매장명 : 용천통닭-월곡점\n-  주문 내역 : 통두마리 x 1\n-  배\n'
    if "주문 접수 안내" in text:

        timezone_kst = timezone(timedelta(hours=9))
        datetime_utc2 = datetime.now(timezone_kst)
        format = '%Y-%m-%d'
        str_datetime = datetime.strftime(datetime_utc2, format)
        
        pattern = re.compile("정상 접수되어, \d+")
        tet = pattern.search(text).group()
        xx = tet.replace('정상 접수되어, ',"")

        pattern2 = re.compile("매장명 : \S+")
        tet2 = pattern2.search(text).group()
        MarketName = tet2.replace('매장명 : ',"")
        print(xx)
        print(MarketName)

        find_WTime(date = str_datetime,time = int(xx),MarketName = MarketName)

    # if "익스프레스 주문 안내" in text2:

    #     timezone_kst = timezone(timedelta(hours=9))
    #     datetime_utc2 = datetime.now(timezone_kst)
    #     format = '%Y-%m-%d'
    #     str_datetime = datetime.strftime(datetime_utc2, format)
        
    #     pattern = re.compile("주문이 \d+")
    #     tet = pattern.search(text2).group()
    #     xx = tet.replace('주문이 ',"")

    #     print(xx)

    #     pattern2 = re.compile("매장명 : \S+")
    #     tet2 = pattern2.search(text2).group()
    #     MarketName = tet2.replace('매장명 : ',"")

    #     # print(MarketName)
    #     find_WTime(date = str_datetime,time = int(xx),MarketName = MarketName)