import requests
import pandas as pd
import json
import math
import time


host_ip = "8.219.67.223"
host_domain = "manage.hinw2a.com"


def read_user_num(lang, token, start_date, end_date):  # 每日阅读人数
    """
    通过数据分析平台获取每日的阅读人数
    调用示例 read_user_num("id", "9b899f7a523caaa04e465e5e0c65ec23", "2024-01-16", "2024-02-18")
    """
    api = "https://analysis-admin.hinovel.com/admin/dashboard/tendency"

    post_data = {
        "lang":lang,
        "os_type":-1,
        "start_date":start_date,
        "end_date":end_date
    }

    headers = {
        "usertoken": token,
        "Content-Type": "application/json"
    }

    rsp = requests.post(url=api, json=post_data, headers=headers).text
    j_rsp = json.loads(rsp)
    list_dates = j_rsp["data"]["read_user"]["xAxis"]
    list_each_day_num = j_rsp["data"]["read_user"]["series"][0]["data"]

    df = pd.DataFrame()
    df["日期"] = list_dates
    df["阅读人数"] = list_each_day_num
    df["阅读人数"] = df["阅读人数"].astype("int")

    return df


def unlock_user_num(lang, token, start_date, end_date):  # 每日解锁人数
    """
    通过数据分析平台获取每日的解锁章节人数
    调用示例 unlock_user_num("id", "9b899f7a523caaa04e465e5e0c65ec23", "2024-01-16", "2024-02-18")
    """
    api = "https://analysis-admin.hinovel.com/admin/dashboard/tendency"

    post_data = {
        "lang":lang,
        "os_type":-1,
        "start_date":start_date,
        "end_date":end_date
    }

    headers = {
        "usertoken": token,
        "Content-Type": "application/json"
    }

    rsp = requests.post(url=api, json=post_data, headers=headers).text
    j_rsp = json.loads(rsp)
    list_dates = j_rsp["data"]["unlock_chapter_user"]["xAxis"]
    list_each_day_num = j_rsp["data"]["unlock_chapter_user"]["series"][0]["data"]

    df = pd.DataFrame()
    df["日期"] = list_dates
    df["解锁人数"] = list_each_day_num
    df["解锁人数"] = df["解锁人数"].astype("int")

    return df


def charge_tongji(cookie, start_date, end_date):  # 充值统计表
    """
    下载：充值统计表（投放金额）
    调用示例 charge_tongji("9b899f7a523caaa04e465e5e0c65ec23", "2024-01-16", "2024-02-18")
    """
    url = f"http://{host_ip}/stat.charge/ajaxList?page=1&limit=10000&date={start_date}%20-%20{end_date}&os_type=-1"
    headers = {
        "Host": host_domain,
        "Cookie": cookie,

    }
    rsp = requests.get(url=url, headers=headers).text
    j_rsp = json.loads(rsp)
    list_per_day_data = j_rsp['data']

    df = pd.DataFrame()
    for d in list_per_day_data:
        dict0 = {}
        dict0["日期"] = d["today"]
        dict0["安装激活数"] = int(d["install_num"])
        dict0["新增用户数"] = int(d["new_user_num"])
        dict0["总订单数"] = int(d["order_all_num"])
        dict0["成功订单数"] = int(d["order_success_num"])
        dict0["成功比例"] = dict0["成功订单数"] / dict0["总订单数"]
        
        try:
            dict0["广告花费"] = float(d["advert_amount"])
        except:
            dict0["广告花费"] = 0

        dict0["当日充值额"] = d["today_pay"]
        try:
            dict0["当日充值额占比"] = d["today_pay"] / dict0["广告花费"]
        except:
            dict0["当日充值额占比"] = "-"

        dict0["7天内充值额"] = d["day7_pay"]
        try:
            dict0["7天内充值额占比"] = d["day7_pay"] / dict0["广告花费"]
        except:
            dict0["7天内充值额占比"] = "-"

        dict0["1月内充值额"] = d["month1_pay"]
        try:
            dict0["1月内充值额占比"] = d["month1_pay"] / dict0["广告花费"]
        except:
            dict0["1月内充值额占比"] = "-"

        dict0["2月内充值额"] = d["month2_pay"]
        try:
            dict0["2月内充值额占比"] = d["month2_pay"] / dict0["广告花费"]
        except:
            dict0["2月内充值额占比"] = "-"

        dict0["3月内充值额"] = d["month3_pay"]
        try:
            dict0["3月内充值额占比"] = d["month3_pay"] / dict0["广告花费"]
        except:
            dict0["3月内充值额占比"] = "-"

        dict0["4月内充值额"] = d["month4_pay"]
        try:
            dict0["4月内充值额占比"] = d["month4_pay"] / dict0["广告花费"]
        except:
            dict0["4月内充值额占比"] = "-"

        dict0["5月内充值额"] = d["month5_pay"]
        try:
            dict0["5月内充值额占比"] = d["month5_pay"] / dict0["广告花费"]
        except:
            dict0["5月内充值额占比"] = "-"

        dict0["半年内充值额"] = d["month6_pay"]
        try:
            dict0["半年内充值额占比"] = d["month6_pay"] / dict0["广告花费"]
        except:
            dict0["半年内充值额占比"] = "-"

        dict0["1年内充值额"] = d["month12_pay"]
        try:
            dict0["1年内充值额占比"] = d["month12_pay"] / dict0["广告花费"]
        except:
            dict0["1年内充值额占比"] = "-"

        dict0["总充值额"] = d["total_pay"]
        try:
            dict0["总充值额占比"] = d["total_pay"] / dict0["广告花费"]
        except:
            dict0["总充值额占比"] = "-"

        df0 = pd.DataFrame([dict0])
        df = pd.concat([df, df0])

    df = df.reset_index(drop=True)
    return df


def charge_new(cookie, list_dates):  # 充值分析表
    # 下载充值分析表
    limit = len(list_dates)
    start = list_dates[0]
    end = list_dates[-1]

    url = f"http://manage.hinw2a.com/stat.recharge/ajaxList?page=1&limit={limit}&device_type=0&tdate={start}%20-%20{end}"
    headers = {
        "Cookie": cookie,
    }
    rsp = requests.get(url=url, headers=headers).text
    json_rsp = json.loads(rsp)
    dict_date_info = json_rsp["data"]

    df = pd.DataFrame()
    for day in list_dates:
        dict0 = {}
        dict_day_info = dict_date_info[day]
        dict0["日期"] = dict_day_info["sdate"]
        dict0["充值总额$"] = dict_day_info["all_charge"]
        dict0["充值金币金额$"] = dict_day_info["charge_coin_price"]
        dict0["充值VIP金额$"] = dict_day_info["charge_vip_price"]
        dict0["活跃用户"] = dict_day_info["day_active"]
        dict0["成功付费人数"] = dict_day_info["success_pay_num"]
        dict0["金币成功付费人数"] = dict_day_info["success_pay_coin_num"]
        dict0["VIP成功付费人数"] = dict_day_info["success_pay_vip_num"]
        dict0["付费率"] = dict_day_info["pay_rate"]
        dict0["复购人数"] = dict_day_info["repurchase_num"]
        dict0["复购率"] = dict_day_info["repurchase_rate"]
        dict0["ARPPU值"] = dict_day_info["arppu"]
        dict0["绑定账号数"] = dict_day_info["blind_num"]
        dict0["新用户成功充值总额"] = dict_day_info["new_user_charge_amount"]
        dict0["新用户成功付费人数"] = dict_day_info["new_user_charge_num"]
        dict0["新用户付费率"] = dict_day_info["new_user_charge_rate"]
        dict0["新用户复购人数"] = dict_day_info["new_user_repurchase_num"]
        dict0["新用户复购率"] = dict_day_info["new_user_repurchase_rate"]
        dict0["新用户ARPPU值"] = dict_day_info["new_user_arppu"]
        dict0["总订单数/成功订单数/成功订单率"] = dict_day_info["all_order_success_rate"]

        df = df.append([dict0])

    return df


def app_tongji(cookie, start_date, end_date):  # APP统计表
    """
    获取后台的APP统计表
    调用示例 app_tongji("PHPSESSID=86780a9450d9b29b5cc51d47c446f682", "2024-01-16", "2024-02-18")    
    """
    api = f"http://{host_ip}/stat.appStat/ajaxList?page=1&limit=10000&device_type=0&tdate={start_date}%20-%20{end_date}"
    headers = {
        "Cookie": cookie,
        "Host": host_domain,
        "X-Requested-With": "XMLHttpRequest",
    }
    rsp = requests.get(url=api, headers=headers).text
    dict_rsp = json.loads(rsp)

    list_df0 = []
    for k,v in dict_rsp["data"].items():
        list_df0.append(v)
    df = pd.DataFrame(list_df0)
    df0 = df.copy()
    df_select = pd.DataFrame()
    df_select["日期"] = df0["sdate"]
    df_select["安装激活数"] = df0["install_active"].astype("int")
    df_select["新增用户数"] = df0["new_user_number"].astype("int")
    df_select["绑定账号人数"] = df0["blind_num"].astype("int")
    df_select["绑定账号率"] = df0["blind_rate"]
    df_select["邀请注册人数"] = df0["invite_reg_num"].astype("int")
    df_select["活跃用户"] = df0["active_user"].astype("int")
    df_select["充值总额$"] = df0["all_charge"].astype("float")
    df_select["ARPU值"] = df0["arpu"].astype("float")
    df_select["VIP数"] = df0["vip"].astype("int")
    df_select["充值VIP金额"] = df0["vip_charge"].astype("float")
    df_select["新用户充值金额"] = df0["new_user_charge_amount"].astype("float")
    df_select["消耗金币"] = df0["expend_coin"].astype("float")
    df_select["消耗书券"] = df0["expend_coupon"].astype("float")
    df_select["消耗书币"] = df0["expend_bean"].astype("float")
    df_select["总消耗"] = df0["all_expend"].astype("float")
    df_select["人均消耗总额"] = df0["avg_all_expend"].astype("float")
    df_select["tdate"] = df0["tdate"]

    return df_select


def novel_list(cookie):  # 小说列表
    each_page_amount = 1000
    url = f"https://{host_domain}/stat.book/ajaxList"
    params = {
        "book_source":"-1",
        "page":"1",
        "limit":"10",
        "book_id":"",
        "platform":"-1",
        "author_name":"",
        "check_user_name":"",
        "follow_name":"",
        "status":"-1",
        "update_status":"-1",
        "sign_type":"0",
        "sign_status":"-1",
        "is_free":"-1",
        "preference":"-1",
        "category_id":"0",
        "recommend":"-1",
        "book_relation":"-1",
        "promotion_status":"-1",
        "date":"",#2022-01-27 - 2022-02-08
        "recharge_date":"",
    }

    headers = {
        "Cookie": cookie,
        "Host": host_domain,
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest",
    }

    s = requests.get(url, params=params, headers=headers, verify=False).text
    dict_s = json.loads(s)
    count_num = dict_s["count"]

    # 获得总页数
    page_num = math.ceil(count_num / each_page_amount)  # 向上取整

    df = pd.DataFrame()
    for page in range(1, page_num+1):
        params = {
            "book_source":"-1",
            "page":f"{page}",
            "limit":f"{each_page_amount}",
            "book_id":"",
            "platform":"-1",
            "author_name":"",
            "check_user_name":"",
            "follow_name":"",
            "status":"-1",
            "update_status":"-1",
            "sign_type":"0",
            "sign_status":"-1",
            "is_free":"-1",
            "preference":"-1",
            "category_id":"0",
            "recommend":"-1",
            "book_relation":"-1",
            "promotion_status":"-1",
            "date":"",#2022-01-27 - 2022-02-08
            "recharge_date":"",
        }
        s = requests.get(url, params=params, headers=headers).text
        dict_s = json.loads(s)
        df0 = pd.DataFrame(dict_s["data"])
        df = pd.concat([df, df0])
        # print(page)

    df_copy = df[[
        "book_id",
        "book_pic_oss",
        "content_length",
        "other_name",
        "book_name",
        "book_info",
        "writer_name",
        "has_relation",
        "category_name",
        "status_name",
        "check_user_name",
        "section_total",
        "total_expend",
        "total_recharge",
        "read_rack_finish",
        "total_price",
        "book_source",
        "is_free",
        "money",
        "able_unlock_for_bean",
        "create_time",
        "remark",
    ]].copy()
    df_copy.columns = [
        "ID",
        "封面",
        "封面信息",
        "小说名称(英)",
        "小说名称(中)",
        "书籍信息",
        "作者笔名",
        "关联书籍",
        "分类",
        "状态",
        "审核人",
        "总章节数",
        "总消耗额",
        "充值额",
        "阅读次数/加入书架人数/看完人数",
        "整本售价($)",
        "版权来源",
        "付费方式",
        "千字价格",
        "可书币解锁",
        "上架时间",
        "备注"
    ]
    df_copy["总消耗额"] = df_copy["总消耗额"].astype("float")
    df_copy["充值额"] = df_copy["充值额"].astype("float")
    df_copy["千字价格"] = df_copy["千字价格"].astype("float")

    return df_copy


def book_count(cookie, start_date, end_date):  # 下载书籍统计表
    search_date = f"{start_date} - {end_date}"
    each_page_amount = 1000

    bookCount_url = f"https://{host_ip}/bookCount/ajaxList"  # 下载接口
    params_1 = {
        "page":"1",
        "limit":"10",
        "search_date":search_date, #"2022-01-20 - 2022-02-20"
        "book_id":"",
        "author":"",
        "follow":"",
        "book_type":"-1",
        "book_source":"-1",
        "is_free":"-1",
        "os_type":"-1",
        "status":"-1",
    }

    headers = {
        "Cookie": cookie,
        "Host": host_domain,
    }

    rsp = requests.get(url=bookCount_url, params=params_1, headers=headers, verify=False).text

    dict_rsp = json.loads(rsp)
    count_num = int(dict_rsp["count"])
    # 获得总页数
    page_num = math.ceil(count_num / each_page_amount)  # 向上取整

    df = pd.DataFrame()
    for page in range(1, page_num+1):
        params_2 = {
            "page":f"{page}",
            "limit":f"{each_page_amount}",
            "search_date":search_date,  #"2022-01-20 - 2022-02-20"
            "book_id":"",
            "author":"",
            "follow":"",
            "book_type":"-1",
            "book_source":"-1",
            "is_free":"-1",
            "os_type":"-1",
            "status":"-1",        
        }
        rsp = requests.get(url=bookCount_url, params=params_2, headers=headers, verify=False).text
        dict_rsp = json.loads(rsp)
        list_rsp = dict_rsp["data"]

        for b in list_rsp:
            Dict_0 = {}
            Dict_0["日期"] = b["search_date"]
            Dict_0["书籍ID"] = b["book_id"]
            Dict_0["书籍名称(中)"] = b["book_name"]
            Dict_0[f"书籍名称(英)"] = b["other_name"]
            Dict_0["书籍类型"] = b["book_type_name"]
            Dict_0["跟进人"] = b["follow"]
            Dict_0["成功订单金额"] = b["order_success_amount"]
            Dict_0["金币消耗"] = b["coin_amount"]
            Dict_0["书券消耗"] = b["coupon_amount"]
            Dict_0["书币消耗"] = b["bean_amount"]
            Dict_0["总消耗"] = b["virtual_money_amount"]
            Dict_0["人均消耗金币"] = b["coin_per_num"]
            Dict_0["人均消耗书券"] = b["coupon_per_num"]
            Dict_0["人均消耗书币"] = b["bean_per_num"]
            Dict_0["付费人均充值金额"] = b["order_per_recharge_amount"]
            Dict_0["总耗金额($)"] = b["book_consume"]
            Dict_0["推荐点击次数"] = b["discover_click_num"]
            Dict_0["阅读人数"] = b["read_num"]
            Dict_0["阅读章节次数"] = b["section_user_num"]
            Dict_0["成功订单数"] = b["order_success_num"]
            Dict_0["成功订单率"] = b["order_success_num_rate"]
            Dict_0["总订单数"] = b["order_all_num"]
            Dict_0["成功订单用户数"] = b["order_success_user_num"]
            Dict_0["加入书架数"] = b["rack_add_num"]
            Dict_0["加入书架率"] = b["rack_rate"]
            Dict_0["撤出书架数"] = b["rack_cancel_num"]
            Dict_0["解锁人数"] = b["unlock_num"]
            Dict_0["解锁率"] = b["unlock_rate"]
            Dict_0["付费率"] = b["pay_rate"]
            Dict_0["当前催更人数"] = b["urging_num"]
            Dict_0["总催更数"] = b["urging_all_num"]
            Dict_0["当日追更人数"] = b["pursue_num"]
            Dict_0["总追更人数"] = b["pursue_all_num"]
            Dict_0["总看完人数"] = b["over_num"]
            Dict_0["纠错次数"] = b["error_num"]
            Dict_0["首读人数"] = b["first_read_num"]
            Dict_0["首充人数"] = b["first_pay_num"]
            Dict_0["首读首充人数"] = b["read_pay_num"]
            Dict_0["首读首充金额"] = b["read_pay_amount"]
            Dict_0["首读7充金额"] = b["read_pay7_amount"]
            Dict_0["人均首读7充金额"] = b["per_first_pay7_read_rate"]
            Dict_0["人均首读首充金额"] = b["per_first_pay_read_rate"]
            Dict_0["首读解锁率"] = b["per_first_read_unlock_rate"]
            Dict_0["上架时间"] = b["check_time"]
            df0 = pd.DataFrame([Dict_0])

            df = pd.concat([df, df0])    
    return df


def book_count_down(cookie, start_date, end_date):  # 书籍统计表-导出接口
    api = f"https://{host_ip}/bookCount/exportBookStat/book_id/0/search_date/{start_date}%20-%20{end_date}/book_type/-1/sort/-1/book_source/-1/is_free/-1/follow/"
    headers = {
        "Host": host_domain,
        "Cookie": cookie,
    }
    rsp = requests.get(url=api, headers=headers, verify=False).text

    with open("书籍统计_英语.txt", encoding="utf-8", mode="w") as f:
        f.write(rsp)
    
    time.sleep(1)
    df = pd.read_csv("书籍统计_英语.txt")
    return df


def book_analysis(start_date, end_date, username, password, book_id=""):
    # 广告后台【书籍分析】
    session = requests.Session()

    login_url = 'https://ads.hinw2a.com/api/admin/login.json'
    post_data = {
        "username": username,
        "password": password,
    }
    headers = {
        "X-ads-aid": "hinovel",
        "X-ads-ip": "8.219.67.223",
        "X-ads-timestamp": f"{int(time.time())}",
    }
    response = session.post(login_url, json=post_data, headers=headers)
    access_token = response.json()['data']['access_token']  # 提取 access_token

    base_url = "https://ads.hinw2a.com/api/lighthouse/ad_book_analysis.json"
    params = {
        "client_type": "",
        "ad_channel": "",
        "lang": "en",
        "book_id": f"{book_id}",
        "date_ranges": f"{start_date}_{end_date}",
        "user_scope": "valid_user",
        "valid_recovery_day": "90",
        "sort_by": "desc",
        "sort_field": "total_roi",
        "page": "1",
        "limit": "10000"
    }

    headers = {
        "X-ads-aid": "hinovel",
        "X-ads-ip": "8.219.67.223",
        "X-ads-timestamp": f"{int(time.time())}",
        "Authorization": f"Bearer {access_token}",
    }
    rsp = session.get(url=base_url, params=params, headers=headers).json()
    df = pd.DataFrame(rsp['data']['list'])
    return df

def book_retention_new(cookie: str, book_id: int, start: str, end: str) -> pd.DataFrame:
    # 获取书籍留存数据，返回DataFrame
    api = f"https://manage.hinw2a.com/BookRetention/bookDetail"
    params = {
        "page": 1,
        "limit": 20,
        "book_id": book_id,
        "date": f"{start} - {end}", 
        "user_type": 0   # 0: 全部用户, 1: 新读者, 2: 活跃老读者, 3: 休眠老读者
    }
    headers = {
        "Cookie": cookie,
        "X-Requested-With": "XMLHttpRequest"
    }

    rsp = requests.get(url=api, params=params, headers=headers).json()
    count = int(rsp["count"])
    total_page = (count - 1) // 20 + 1

    for page in range(1, total_page + 1):
        print(f"正在处理第{page}页，共{total_page}页")
        params["page"] = page
        rsp = requests.get(url=api, params=params, headers=headers).json()
        df_page = pd.DataFrame(rsp["data"])
        if page == 1:
            df = df_page.copy()
        else:
            df = pd.concat([df, df_page], ignore_index=True)

    df[["stay_rate", "follow_rate"]] = df[["stay_rate", "follow_rate"]].applymap(lambda x: float(re.sub(r"<span class='color_green'>(.*?)%</span>", r"\1", str(x))) if isinstance(x, str) else x)
    df["num_day_stay"] = df["list_order"] - 1

    # list_order
    # current_chapter_users_total # 各章阅读人数
    # until_chapter_users_total	
    # stay_retention_users
    # stay_rate
    # follow_rate
    # num_day_stay
    return df
