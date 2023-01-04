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

if __name__ == "__main__":
    print("sd")
