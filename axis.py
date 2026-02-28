import requests
import pandas as pd


url_cookie = "https://raw.githubusercontent.com/mjqgh/modules/refs/heads/main/cookies.json"  # 从在线json中获取cookie
dict_cookies = requests.get(url_cookie).json()
cookie_axis = dict_cookies["axis"]

def pn_book_tongji(start_date, end_date, cookie=None):
    # 小说统计表
    global cookie_axis
    if cookie==None:
        cookie=cookie_axis
        
    def book_tongji(cookie, start_date, end_date, page_num):
        api = "http://aikan-admin.thnovel.com/BookStat/bookDayFullStat"
        post_data = {
            "page": page_num,
            "limit": 100,
            "date": f"{start_date} ~ {end_date}",
            "keyword": "",
            "lang": "en",
            "platform": ""
        }
        headers = {
            "Cookie": cookie,
            "X-Requested-With": "XMLHttpRequest"
        }
        rsp = requests.post(url=api, headers=headers, data=post_data).json()
        return rsp

    total = book_tongji(cookie=cookie, start_date=start_date, end_date=end_date, page_num=1)["data"]["paging_data"]["total"]
    total_page_num = (total + 99) // 100  # 整数向上取整（不需额外导入）

    df_total = pd.DataFrame()
    for page_num in range(1, total_page_num+1):
        # print(page_num)
        list_items = book_tongji(cookie=cookie, start_date=start_date, end_date=end_date, page_num=page_num)["data"]["items"]
        df_items = pd.DataFrame(list_items)
        df_total = pd.concat([df_total, df_items])

    return df_total

