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
        time.sleep(10)
        print("쓰레딩....")
        Find_All_Order()

@app.post('/wait-time')
def Waittime(item : Item):
    
    Insert_WaitTime(item.date,item.message)
    return item

@app.post('/depo')
def Depo(item : Item):
    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)
    format = '%Y-%m-%d'
    str_datetime = datetime.strftime(datetime_utc2, format)

    pattern = re.compile("입금\S+원")
    tet = pattern.search(item.message).group()
    money = tet.replace("입금","").replace("원","").replace(",","")
    print(item.message)
    Find_Depo(str_datetime, int(money))
    return item

@app.get('/Thread_Start')
def find_User_Data2(background_tasks: BackgroundTasks = None):
    background_tasks.add_task(Times)
    return "result"