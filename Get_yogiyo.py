import requests
from Ordersdatas import *
from Make_Datas import *
from DBMaker import *
from AccessToken import *


def Find_Depo(date, money):
    find_money(date,money)

def get_Yogiyo(category, lat, lng, own_delivery_only):
    header = {"x-apikey": 'iphoneap',
              "x-apisecret": 'fe5183cc3dea12bd0ce299cf110a75a2'}

    url = f"https://www.yogiyo.co.kr/api/v1/restaurants-geo/?category={category}&items=60&lat={lat}&lng={lng}&order=rank&own_delivery_only={own_delivery_only}&order=distance&page=0&search="
    response = requests.get(url, headers=header)
    Get_json = response.json()
    Get_json['restaurants']
    return Get_json


if __name__ == "__main__":
    rt = get_Yogiyo("전체",37.5347556106622,127.114906298514,False)
    
    print(rt)
