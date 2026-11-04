import requests
import pandas as pd
from io import StringIO


url_cookie = "https://raw.githubusercontent.com/mjqgh/modules/refs/heads/main/cookies.json"  # 从在线json中获取cookie
dict_cookies = requests.get(url_cookie).json()
cookie_zip = dict_cookies["zip"]

def zippy_book_tongji(start_date, end_date, cookie=None):
    # 小说统计表
    global cookie_zip
    if cookie==None:
        cookie=cookie_zip

    api_export = f"https://zippy.thnovel.com/BookStat/exportBookDayFullStat?date={start_date}%20~%20{end_date}&keyword=&lang=en&platform="
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Cookie": cookie
    }
    response = requests.get(api_export, headers=headers)
    # 保存到一个df
    df = pd.read_csv(StringIO(response.text))
    return df
