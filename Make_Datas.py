def Wait_Time_Data(userId,UserName,Time,Market_Name):

    datas = {
            "to": userId,
            "messages": [
                {
                    "type": "flex",
                    "altText": "Wait Time",
                    "contents": {
                        "type": "carousel",
                        "contents": [
                            {#시작
                                "type": "bubble",
                                "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "md",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "FastFood",
                                        "wrap": True,
                                        "weight": "bold",
                                        "gravity": "center",
                                        "size": "4xl",
                                        "align": "center",
                                        "color": "#B266FF"
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
                                            "layout": "baseline",
                                            "spacing": "sm",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": "ชื่อลูกค้า",#고객명
                                                "color": "#aaaaaa",
                                                "size": "sm",
                                                "flex": 1
                                            },
                                            {
                                                "type": "text",
                                                "wrap": True,
                                                "size": "sm",
                                                "color": "#666666",
                                                "flex": 4,
                                                "align": "end",
                                                "text": UserName
                                            }
                                            ]
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "spacing": "sm",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": "ชื่อร้านที่สั่ง",#업체명
                                                "color": "#aaaaaa",
                                                "size": "sm",
                                                "flex": 2
                                            },
                                            {
                                                "type": "text",
                                                "wrap": True,
                                                "size": "sm",
                                                "color": "#666666",
                                                "flex": 6,
                                                "align": "end",
                                                "text": Market_Name
                                            }
                                            ]
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "spacing": "sm",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": "เวลาที่ต้องรอ",
                                                "color": "#aaaaaa",
                                                "size": "sm",
                                                "flex": 5
                                            },
                                            {
                                                "type": "text",
                                                "text": f"{Time} นาที",
                                                "wrap": True,
                                                "color": "#6666FF",
                                                "size": "xl",
                                                "flex": 5,
                                                "align": "end",
                                                "weight": "bold"
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
                                        "type": "text",
                                        "text": f"{UserName} ดำเนินการสั่งเรียบร้อยแล้วนะคะกรุณรอ ประมาณ  {Time}  นาทีนะคะคุณลูกค้า หากได้รับอาหารแล้ว กรุณาส่งรูปภาพให้แอดมินด้วยนะคะ",
                                        "wrap": True,
                                        "margin": "xxl"
                                    }
                                    ]
                                }
                            } #  끝
                        ]
                    }

                }
            ]
        }

    return datas

def Shop_Link(userId,point,Market_Name):

    datas = {
            "to": userId,
            "messages": [
                {
                    "type": "flex",
                    "altText": "ข้อมูลการยกเลิก!",
                    "contents": {
                        "type": "carousel",
                        "contents": [
                            {
                                "type": "bubble",
                                "header": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "ข้อมูลการยกเลิก",
                                        "size": "xxl",
                                        "wrap": True,
                                        "gravity": "center",
                                        "align": "center",
                                        "style": "normal",
                                        "weight": "bold",
                                        "decoration": "none",
                                        "color": "#CC0000"
                                    },
                                    {
                                        "type": "separator"
                                    },
                                    {
                                        "type": "text",
                                        "text": 'ชื่อร้านที่ยกเลิก',
                                        "wrap": True,
                                        "gravity": "center",
                                        "align": "center",
                                        "size": "xxl",
                                        "style": "normal",
                                        "weight": "bold",
                                        "decoration": "none",
                                    },
                                    {
                                        "type": "text",
                                        "text": f"{Market_Name}",
                                        "wrap": True,
                                        "gravity": "center",
                                        "align": "center",
                                        "style": "normal",
                                        "weight": "bold",
                                        "decoration": "none",
                                    },
                                    ]
                                },
                                "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "คำสั่งซื้อของคุณร้านอาหารได้ยกเลิก\nแล้วค่ะ",
                                        "wrap": True,
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": "ขออภัยในความไม่สะดวกนะคะ หากทำให้ลูกค้าผิดหวังในการรอทานอาหาร",
                                        "wrap": True,
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": "จำนวนเงินที่ลูกค้ามีอยู่จะถูกเปลี่ยนเป็น",
                                        "wrap": True,
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"พ้อยท์ {point}",
                                        "wrap": True,
                                        "align": "center",
                                        "size": "xl",
                                        "color": "#1DB446",
                                        "weight": "bold"
                                    },
                                    {
                                        "type": "text",
                                        "text": "ลูกค้าสามารถสั่งอาหารตอนไหนก็ได้ค่ะ",
                                        "wrap": True,
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": "เมื่อลูกค้าสั่งอาหารระบบจะหักจากพ้อยท์อัตโนมัตินะคะ หรือลูกค้าต้องการคืนเงินก็ได้ค่ะ",
                                        "wrap": True,
                                        "align": "center"
                                    }
                                    ]
                                },
                                "footer": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "button",
                                        "style": "primary",
                                        "color": "#B266FF",
                                        "margin": "xxl",
                                        "action": {
                                        "type": "uri",
                                        "label": "หาร้านอาหารอื่นๆ",
                                        "uri": "https://liff.line.me/1657404178-vbEl737y",
                                        }
                                    }
                                    ]
                                }
                                }
                        ]
                    }

                }
            ]
        }

    return datas


def Make_Base(userId,point):

    datas = {
            "to": userId,
            "messages": [
                {
                    "type": "flex",
                    "altText": "ข้อมูลการยกเลิก!",
                    "contents": {
                        "type": "carousel",
                        "contents": [
                            Time_30(point)
                        ]
                    }
                }
            ]
    }
    return datas

def Time_30(point):
    datas = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "ข้อมูลการยกเลิก",
                    "weight": "bold",
                    "size": "xxl",
                    "color": "#FF3333"
                }
                ],
                "alignItems": "center"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "xxl",
                "spacing": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "포인트 3000",
                    "contents": [
                    {
                        "type": "span",
                        "text": "พ้อยท์"
                    },
                    {
                        "type": "span",
                        "text": str(format(int(point), ',')),
                        "color": "#1DB446",
                        "weight": "bold",
                        "size": "xl"
                    }
                    ]
                }
                ],
                "alignItems": "center"
            },
            {
                "type": "separator",
                "margin": "md"
            },
            {
                "type": "text",
                "text": "ขออภัยค่ะคุณลูกค้าหลังจาก",
                "contents": [
                {
                    "type": "span",
                    "text": "ขออภัยค่ะคุณลูกค้า"
                }
                ],
                "align": "center"
            },
            {
                "type": "text",
                "text": "หลังจาก  30",
                "align": "center",
                "contents": [
                {
                    "type": "span",
                    "text": "หลังจาก  "
                },
                {
                    "type": "span",
                    "text": "30",
                    "color": "#FF3333",
                    "weight": "bold",
                    "size": "xl"
                }
                ]
            },
            {
                "type": "text",
                "text": "นาทีของการสั่งอาหาร",
                "margin": "none",
                "align": "center"
            },
            {
                "type": "text",
                "text": "รายการจะถูกยกเลิกอัตโนมัติเพราะลูกค้าโอนเงินล่าช้า",
                "margin": "none",
                "wrap": True,
                "align": "center"
            },
            {
                "type": "text",
                "text": "กรุณาเลือกสั่งรายการอาหารใหม่อีกครั้งค่ะ",
                "margin": "none",
                "wrap": True,
                "align": "center"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "button",
                    "action": {
                    "type": "uri",
                    "label": "หาร้านอาหารอื่นๆ",
                    "uri": "https://liff.line.me/1657404178-vbEl737y"
                    },
                    "style": "primary",
                    "color": "#B266FF"
                }
                ],
                "margin": "lg"
            }
            ]
        },
        "styles": {
            "footer": {
            "separator": True
            }
        }
    }
    return datas

if __name__ == "__main__":
    print("sd")
