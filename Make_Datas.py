from DBMaker import find_Account

def Make_dics(get_List, lists):
    for i in lists:
        get_List.append(i)
    return get_List


def Set_Options(x):
    datas = [{
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "text",
                "text": "옵션메뉴",  # 옵션메뉴
                "size": "sm",
                "color": "#1DB446"
            },
            {
                "type": "text",
                "text": x['optionName'],
                "align": "end",
                "size": "sm",
                "color": "#111111",
                "wrap": True
            }
        ]
    },
        {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "text",
                "text": "옵션명",  # 옵션명
                "size": "sm",
                "color": "#1DB446"
            },
            {
                "type": "text",
                "text": x['subOptionName'],
                "size": "sm",
                "color": "#111111",
                "align": "end",
                "wrap": True
            }
        ]
    },
        {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "text",
                "text": "옵션가격",  # 옵션가격
                "size": "sm",
                "color": "#1DB446"
            },
            {
                "type": "text",
                "text": format(x['subOptionPrice'], ',d') + ' ￦',
                "size": "sm",
                "color": "#111111",
                "align": "end"
            }
        ]
    },
    ]

    return datas


def Set_Dics(menu, i):
    data = [{
        "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "음식이름",  # 음식이름
                        "size": "sm",
                        "color": "#555555"
                    },
                    {
                        "type": "text",
                        "text": menu['menu_name'],
                        "size": "sm",
                        "color": "#111111",
                        "align": "end",
                        "wrap": True
                    }
                ]
    },

        {
        "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "수량",  # 수량
                        "size": "sm",
                        "color": "#555555"
                    },
                    {
                        "type": "text",
                        "text": str(i['quantity']) + "개",
                        "size": "sm",
                        "color": "#111111",
                        "align": "end"
                    }
                ]
    },
        {
        "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "가격",  # 가격
                        "size": "sm",
                        "color": "#555555"
                    },
                    {
                        "type": "text",
                        "text": format(int(menu['price']), ',d') + ' ￦',
                        "size": "sm",
                        "color": "#111111",
                        "align": "end"
                    }
                ]
    },
        {
        "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "총가격",  # 총가격
                        "size": "sm",
                        "color": "#555555"
                    },
                    {
                        "type": "text",
                        "text": format(int(i['totalPrice']), ',d') + ' ￦',
                        "size": "sm",
                        "color": "#111111",
                        "align": "end"
                    }
                ]
    }]
    return data


def Make_OrderList(UserId, UserName, OrderData, cart, Menu_Data, options_fee, totals, Order_Code):
    datas = {
        "to": UserId,
        "messages": [
            {
                "type": "flex",
                "altText": "ข้อมูลการสั่งซื้อ",  # 주문정보
                "contents": {
                    "type": "carousel",
                    "contents": [
                        {  # flax1
                            "type": "bubble",
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "FastFood",
                                        "weight": "bold",
                                        "color": "#1DB446",
                                        "size": "sm"
                                    },
                                    {
                                        "type": "text",
                                        "text": "ข้อมูลลูกค้า",  # 고객정보
                                        "weight": "bold",
                                        "size": "xxl",
                                        "margin": "md"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "margin": "xxl",
                                        "spacing": "sm",
                                        "contents": [
                                            {
                                                "type": "separator",
                                                "margin": "xxl"
                                            },
                                            {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": "ชื่อผู้สั่งซื้อ",  # 주문자명
                                                        "size": "sm",
                                                        "color": "#555555"
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": UserName,
                                                        "size": "sm",
                                                        "color": "#111111",
                                                        "align": "end",
                                                        "wrap": True
                                                    }
                                                ],
                                                "margin": "xxl"
                                            },
                                            {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": "ที่อยู่",  # 주소
                                                        "size": "sm",
                                                        "color": "#555555"
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": OrderData['address'] + ' ' + OrderData['addressDetail'] if OrderData['address'] != "" and OrderData['addressDetail'] != "" else "주문정보 입력 안됨.",
                                                        "size": "sm",
                                                        "color": "#111111",
                                                        "align": "end",
                                                        "wrap": True
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": "รหัสผ่านชั้น 1",
                                                        "size": "sm",
                                                        "color": "#555555"
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": OrderData['firstFloorEntranceCode'] if OrderData['firstFloorEntranceCode'] != "" else "주문정보 입력 안됨.",
                                                        "size": "sm",
                                                        "color": "#111111",
                                                        "align": "end",
                                                        "wrap": True
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": "รายละเอียดการสั่งซื้อ",  # 주문사항
                                                        "size": "sm",
                                                        "color": "#555555"
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": OrderData['deliveryMessage'],
                                                        "size": "sm",
                                                        "color": "#111111",
                                                        "align": "end",
                                                        "wrap": True
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": "หมายเลขโทรศัพท์",  # 전화번호
                                                        "size": "sm",
                                                        "color": "#555555"
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": OrderData['phone'],
                                                        "size": "sm",
                                                        "color": "#111111",
                                                        "align": "end",
                                                        "wrap": True
                                                    }
                                                ]
                                            }
                                        ]
                                    },
                                    {
                                        "type": "separator",
                                        "margin": "xxl"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "margin": "md",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "เลขที่ใบสั่งซื้อ",  # 주문번호
                                                "size": "xs",
                                                "color": "#aaaaaa",
                                                "flex": 0
                                            },
                                            {
                                                "type": "text",
                                                "text": str(Order_Code),
                                                "color": "#aaaaaa",
                                                "size": "xs",
                                                "align": "end"
                                            }
                                        ]
                                    }
                                ]
                            },
                            "styles": {
                                "footer": {
                                    "separator": True
                                }
                            }
                        },  # flax1
                        {  # flax2
                            "type": "bubble",
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "FastFood",
                                        "weight": "bold",
                                        "color": "#1DB446",
                                        "size": "sm"
                                    },
                                    {
                                        "type": "text",
                                        "text": "주문정보",  # 주문정보
                                        "weight": "bold",
                                        "size": "xxl",
                                        "margin": "md"
                                    },
                                    {
                                        "type": "separator",
                                        "margin": "none"
                                    },
                                    {
                                        "type": "text",
                                        "text": cart[0]['storeName'],
                                        "size": "md",
                                        "align": "center",
                                        "gravity": "center",
                                        "margin": "lg",
                                        "weight": "bold",
                                        "wrap": True
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "spacing": "sm",
                                        "contents": [
                                            {
                                                "type": "separator",
                                                "margin": "lg"
                                            },
                                            {
                                                "type": "box",
                                                "layout": "vertical",
                                                "spacing": "sm",
                                                "contents": Menu_Data},  # 메뉴명
                                            {
                                                "type": "separator"
                                            },

                                        ]
                                    },
                                    {
                                        "type": "separator",
                                        "margin": "xxl"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "margin": "md",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "เลขที่ใบสั่งซื้อ",  # 주문번호
                                                "size": "xs",
                                                "color": "#aaaaaa",
                                                "flex": 0
                                            },
                                            {
                                                "type": "text",
                                                "text": str(Order_Code),
                                                "color": "#aaaaaa",
                                                "size": "xs",
                                                "align": "end"
                                            }
                                        ]
                                    }
                                ]
                            },
                            "styles": {
                                "footer": {
                                    "separator": True
                                }
                            }
                        }  # flax2
                    ]
                }
            }
        ]
    }
    return datas


def Make_DD(userId, Total_pay, deliver_fee, Total_Count, UserName, Order_Code, Service_Money):
    Account = find_Account()
    datas = {
        "to": userId,
        "messages": [
            {
                "type": "flex",
                "altText": "ส่งคำสั่งซื้อของคุณเรียบร้อยแล้ว!",
                "contents": {
                    "type": "carousel",
                    "contents": [
                        {  # 시작
                            "type": "bubble",
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "FASTFOOD",
                                        "weight": "bold",
                                        "color": "#000000",
                                        "size": "sm"
                                    },
                                    {
                                        "type": "text",
                                        "text": "ยอดเงินที่ต้องชำระ",  # 주문금액
                                        "weight": "bold",
                                        "size": "xxl",
                                        "margin": "md",
                                        "color": "#1DB446"
                                    },
                                    {
                                        "type": "separator",
                                        "margin": "xxl"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "margin": "xxl",
                                        "spacing": "sm",
                                        "contents": [
                                            {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": "ราคารวม",  # 총가격
                                                        "size": "sm",
                                                        "color": "#555555",
                                                        "flex": 0
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": format(Total_pay, ',d') + ' ￦',
                                                        "size": "sm",
                                                        "color": "#111111",
                                                        "align": "end",
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": "ค่าจัดส่ง",  # 배송비
                                                        "size": "sm",
                                                        "color": "#555555",
                                                        "flex": 0
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": format(deliver_fee, ',d') + ' ￦',
                                                        "size": "sm",
                                                        "color": "#111111",
                                                        "align": "end"
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": "ค่าบริการ",  # 서비스요금
                                                        "size": "sm",
                                                        "color": "#555555",
                                                        "flex": 0
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": f"{format(Service_Money, ',d')} ￦",
                                                        "size": "sm",
                                                        "color": "#111111",
                                                        "align": "end"
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "separator",
                                                "margin": "xxl"
                                            },
                                            {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": "รวมจ่ายทั้งหมด",  # 총금액
                                                        "weight": "bold"
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": '￦ ' + format(Total_Count, ',d'),
                                                        "align": "end",
                                                        "weight": "bold",
                                                        "color": "#1823b7"
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "separator"
                                            },
                                            {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "margin": "xxl",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": "เลขที่บัญชี",  # 계좌번호
                                                        "size": "sm",
                                                        "color": "#111111"
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": str(Account["Account_Name"]),
                                                        "size": "sm",
                                                        "color": "#037bfc",
                                                        "align": "end",
                                                        "wrap": True
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": "ธนาคาร",  # 은행명
                                                        "size": "sm",
                                                        "color": "#111111"
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": str(Account["Bank_Name"]),
                                                        "size": "sm",
                                                        "color": "#037bfc",
                                                        "align": "end"
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": "ชื่อบัญชีเกาหลี",  # 예금주
                                                        "size": "sm",
                                                        "color": "#111111"
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": str(Account["Account_Number"]),
                                                        "size": "sm",
                                                        "color": "#037bfc",
                                                        "align": "end"
                                                    }
                                                ]
                                            }
                                        ]
                                    },
                                    {
                                        "type": "separator",
                                        "margin": "xxl"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "margin": "md",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "เราขออภัยคุณลูกค้าหากมีค่าบริการเพิ่มเติมนอกเหนือจากค่าบริการจัดส่งที่แสดงขึ้นอยู่กับระยะทางในการจัดส่ง ",  # 주문코드
                                                "size": "sm",
                                                "color": "#037bfc",
                                                "flex": 0,
                                                "wrap": True
                                            },
                                        ]
                                    },
                                    {
                                        "type": "separator",
                                        "margin": "xxl"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "margin": "md",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "เลขที่ใบสั่งซื้อ",  # 주문코드
                                                "size": "xs",
                                                "color": "#aaaaaa",
                                                "flex": 0
                                            },
                                            {
                                                "type": "text",
                                                "text": str(Order_Code),
                                                "color": "#aaaaaa",
                                                "size": "xs",
                                                "align": "end"
                                            }
                                        ]
                                    }
                                ]
                            },
                            "styles": {
                                "footer": {
                                    "separator": True
                                }
                            }
                        },  # 끝
                        {
                            "type": "bubble",
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "maxHeight": "300px",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "❤FASTFOOD❤",
                                        "wrap": True,
                                        "align": "center",
                                        "gravity": "center"
                                    },
                                    {
                                        "type": "text",
                                        # 위 계좌번호로 입금 해주세요🙏🏻\n\n입금 확인후 {UserName}님 에게  음식 배달을 시작합니다
                                        "text": f"{UserName} กรุณาฝากเงินเข้าเลขที่บัญชี\nหลังจากยืนยันการชำระเงิน\nเราจะเริ่มจัดส่งอาหารไปยังคุณลูกค้าทันที🥰  \n\n🍝🍲🍤🦪🍙🎂🍕🍟🌮🥘🍰🍱🍣🥟🍜🍦🧁🍿🧋🌭🍔🌯",
                                        "wrap": True,
                                        "align": "center",
                                        "gravity": "center"
                                    }
                                ]
                            },
                            "styles": {
                                "footer": {
                                    "separator": True
                                }
                            }
                        }
                    ]
                }

            }
        ]
    }
    return datas


if __name__ == "__main__":
    print("sd")
