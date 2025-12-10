import requests
import pandas as pd
import json
import math
import time
import re
from lxml import etree


host_ip = "8.219.67.223"
host_domain = "manage.hinw2a.com"

j_cookies = requests.get("https://raw.githubusercontent.com/mjqgh/modules/refs/heads/main/cookies.json").json()
cookie_hn = j_cookies["hn"] 


def each_day_adspend(start_date, end_date, access_token):
    # 广告后台【每日消耗】
    base_url = "https://ads.hinw2a.com/api/datamanage/list.json"
    post_data = {date_ranges: f"{start_date}_{end_date}"}

    headers = {
        "X-ads-aid": "hinovel",
        "X-ads-ip": "8.219.67.223",
        "X-ads-timestamp": f"{int(time.time())}",
        "Authorization": f"Bearer {access_token}",
    }
    rsp = requests.post(url=base_url, data=post_data, headers=headers).json()
    df = pd.DataFrame(rsp['data'])
    return df

def hn_book_info(hn_id):
    # 获取hn小说的书籍信息
    url = f"https://manage.hinw2a.com/stat.book/ajaxList?book_id={hn_id}"
    headers = {
        "Cookie": cookie_hn
    }
    rsp = requests.get(url, headers=headers).json()
    # if rsp["data"]["total"] == 0:
    #     return None
    dict_rsp = rsp["data"][0]
    # begin_cost：卡点锁章
    # book_info：书籍信息
    return dict_rsp

def change_begin_cost(cookie, hn_id, begin_cost):
    # 更改翻译书卡点锁章
    api = f"https://manage.hinw2a.com/stat.book/edit/book_id/{hn_id}/channel_type/1"
    headers = {"Cookie": cookie}
    rsp = requests.get(url=api, headers=headers).text
    html = etree.HTML(rsp)

    begin_cost = begin_cost  # 起点收费章节，需要设置

    rate = html.xpath('//input[@name="rate"]/@value')[0]  # rate 
    divide_proportions = html.xpath('//input[@name="divide_proportions"]/@value')[0]  # 分成比例 
    length_type = html.xpath('//input[@name="length_type"]/@value')[0]
    other_name = html.xpath('//input[@name="other_name"]/@value')[0]  # 书籍别名
    book_name = html.xpath('//input[@name="book_name"]/@value')[0]  # 书籍名称
    writer_name = html.xpath('//input[@name="writer_name"]/@value')[0]  # 作者名称
    comment_avg_score = html.xpath('//input[@name="comment_avg_score"]/@value')[0]  # 书籍评分
    file = "no"
    book_pic = html.xpath('//input[@name="book_pic"]/@value')[0]  # 书籍封面
    book_pic_oss = html.xpath('//input[@name="book_pic_oss"]/@value')[0]  # 书籍封面oss地址
    book_water_pic = html.xpath('//input[@name="book_water_pic"]/@value')[0]  # 书籍水印封面
    author_id = html.xpath('//input[@name="author_id"]/@value')[0]  # 作者ID
    try:
        book_desc = html.xpath('//textarea[@name="book_desc"]/text()')[0]  # 书籍简介
    except:
        book_desc = ""
    preference = html.xpath('//input[@name="preference"][@checked]/@value')[0]  # 书籍偏好类型
    category_id = html.xpath('//select[@name="category_id"]/option[@selected]/@value')[0]  # 书籍分类

    money = html.xpath('//input[@name="money"]/@value')[0]  # 千字单价
    status = html.xpath('//input[@name="status"][@checked]/@value')[0]  # 上架状态
    update_status = html.xpath('//input[@name="update_status"][@checked]/@value')[0]  # 连载状态

    str_labels = re.compile(r"setValue\(\[(.*?)\]").search(rsp).group(1)
    str_list_labels = "[" + str_labels + "]"
    list_labels = eval(str_list_labels)  # 书籍标签

    str_label_value = ""
    for i in list_labels:
        label_value = i['value']
        str_label_value += str(label_value) + ","
    str_label_value = str_label_value[:-1]  # 去掉最后一个逗号

    is_free = html.xpath('//input[@name="is_free"][@checked]/@value')[0]  # 是否免费
    is_ad_unlock = html.xpath('//input[@name="is_ad_unlock"][@checked]/@value')[0]  # 是否广告解锁
    book_source = html.xpath('//input[@name="book_source"][@checked]/@value')[0]  # 书籍来源
    section_num = html.xpath('//input[@name="section_num"]/@value')[0]  # 章节数
    try:
        remark = html.xpath('//textarea[@name="remark"]/text()')[0]  # 备注
    except:
        remark = ""
    shareable = html.xpath('//input[@name="shareable"][@checked]/@value')[0]  # 是否允许分享
    recommend = html.xpath('//input[@name="recommend"][@checked]/@value')[0]  # 推荐状态
    add_types = "0"
    advances = html.xpath('//input[@name="advances"]/@value')[0]  # 是否预收
    surplus_advance_charge = html.xpath('//input[@name="surplus_advance_charge"]/@value')[0]  # 预收剩余可收费章节数
    advance_charge = html.xpath('//input[@name="advance_charge"]/@value')[0]  # 预收已收费章节数
    content_grade = html.xpath('//input[@name="content_grade"][@checked]/@value')[0]  # 内容分级
    adult_content_level = html.xpath('//input[@name="adult_content_level"][@checked]/@value')[0]  # 成人内容等级
    able_unlock_for_bean = html.xpath('//input[@name="able_unlock_for_bean"][@checked]/@value')[0]  # 是否允许豆解锁
    adult_chapter_begin = html.xpath('//input[@name="adult_chapter_begin"]/@value')[0]  # 成人章节开始章节数
    del_relation_copyright_platform = "0"  # 删除关联版权平台
    book_id = html.xpath('//input[@name="book_id"]/@value')[0]  # 书籍ID

    data = {
        "rate": rate,
        "divide_proportions": divide_proportions,
        "length_type": length_type,
        "other_name": other_name,
        "book_name": book_name,
        "writer_name": writer_name,
        "comment_avg_score": comment_avg_score,
        "money": money,
        "begin_cost": begin_cost,
        "status": status,
        "file": file,
        "book_pic": book_pic,
        "book_pic_oss": book_pic_oss,
        "book_water_pic": book_water_pic,
        "author_id": author_id,
        "book_desc": book_desc,
        "preference": preference,
        "category_id": category_id,
        "labels": str_label_value,
        "is_free": is_free,
        "is_ad_unlock": is_ad_unlock,
        "update_status": update_status,
        "book_source": book_source,
        "section_num": section_num,
        "remark": remark,
        "shareable": shareable,
        "recommend": recommend,
        "add_types": add_types,
        "advances": advances,
        "surplus_advance_charge": surplus_advance_charge,
        "advance_charge": advance_charge,
        "content_grade": content_grade,
        "adult_content_level": adult_content_level,
        "able_unlock_for_bean": able_unlock_for_bean,
        "adult_chapter_begin": adult_chapter_begin,
        "del_relation_copyright_platform": del_relation_copyright_platform,
        "book_id": book_id
    }
    # 提交保存书籍信息
    api_save_bookinfo = "https://manage.hinw2a.com/stat.book/ajaxEdit"
    rsp_save = requests.post(url=api_save_bookinfo, headers=headers, data=data).text

    # print(data)
    return rsp_save

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


def book_analysis(start_date, end_date, access_token, book_id=""):
    # 广告后台【书籍分析】
    session = requests.Session()

    # login_url = 'https://ads.hinw2a.com/api/admin/login.json'
    # post_data = {
    #     "username": username,
    #     "password": password,
    # }
    # headers = {
    #     "X-ads-aid": "hinovel",
    #     "X-ads-ip": "8.219.67.223",
    #     "X-ads-timestamp": f"{int(time.time())}",
    # }
    # response = session.post(login_url, json=post_data, headers=headers)
    # access_token = response.json()['data']['access_token']  # 提取 access_token

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

def book_retention_old(cookie: str, book_id: int, start: str, end: str) -> pd.DataFrame:
    api = f"https://manage.hinw2a.com/BookEfficiency/detail?book_id={book_id}&os_type=-1&date={start}%20-%20{end}"
    headers = {"Cookie": cookie}

    rsp = requests.get(url=api, headers=headers).text

    p = re.compile(r"let data ?= ?(.*?);")
    res = p.search(rsp).group(1)
    list_dict_res = eval(res)
    df = pd.DataFrame(list_dict_res)
    df["list_order"] = df["list_order"].astype("int")
    df["chapter_read_num"] = df["chapter_read_num"].astype("int")

    # 锁章转化率
    p_begin_cost = re.compile(r'let begin_cost_section_id = "(.*?)";')
    begin_cost = p_begin_cost.search(rsp).group(1)
    begin_cost_section_id = eval(begin_cost)  # 锁章章节号

    before_cost_num = df.loc[df["list_order"]==begin_cost_section_id-1, "chapter_read_num"].iloc[0]
    begin_cost_num = df.loc[df["list_order"]==begin_cost_section_id, "chapter_read_num"].iloc[0]
    try:
        zhuanhua = round(begin_cost_num / before_cost_num, 2)
    except:
        zhuanhua = 0.00

    df_readers_num = df[["list_order", "chapter_read_num"]].copy()
    df_readers_num = df_readers_num.rename(columns={"list_order": "章节序号", "chapter_read_num": "阅读人数"})

    df_readers_num["是否免费"] = df_readers_num["章节序号"].apply(lambda x: 1 if x < begin_cost_section_id else 0)
    df_readers_num["章节流失阅读人数"] = df_readers_num["阅读人数"] - df_readers_num["阅读人数"].shift(1)
    df_readers_num["章节流失阅读人数"] = df_readers_num["章节流失阅读人数"].fillna(0).astype("int")
    df_readers_num["章节流失率"] = df_readers_num["章节流失阅读人数"] / df_readers_num["阅读人数"].shift(1)
    df_readers_num["章节流失率"] = df_readers_num["章节流失率"].fillna(0)
    df_readers_num["锁章章节号"] = begin_cost_section_id
    df_readers_num["锁章转化率"] = zhuanhua
    # 章节序号 - 阅读人数 - 是否免费 - 章节流失阅读人数 - 章节流失率 - 锁章章节号 - 锁章转化率
    # 最多返回200章节
    return df_readers_num

def get_hi_kadian(cookie: str, hi_id) -> int:
    # 获取小说的付费章节号
    today_str = time.strftime("%Y-%m-%d", time.localtime())

    api = f"https://manage.hinw2a.com/BookRetention/bookDetail?book_id={hi_id}&date={today_str}%20-%20{today_str}&user_type=0"
    headers = {
        "Cookie": cookie
    }
    rsp = requests.get(api, headers=headers).text
    kadian = int(re.compile("付费章节: ?(\d+)").search(rsp).group(1))
    return kadian

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
        # print(f"正在处理第{page}页，共{total_page}页")
        params["page"] = page
        rsp = requests.get(url=api, params=params, headers=headers).json()
        df_page = pd.DataFrame(rsp["data"])
        if page == 1:
            df = df_page.copy()
        else:
            df = pd.concat([df, df_page], ignore_index=True)

    df[["stay_rate", "follow_rate"]] = df[["stay_rate", "follow_rate"]].applymap(lambda x: float(re.sub(r"<span class='color_green'>(.*?)%</span>", r"\1", str(x))) if isinstance(x, str) else x)
    df["num_day_stay"] = df["list_order"] - 1
    df["current_chapter_users_total"] = df["current_chapter_users_total"].astype(int)

    def get_kadian(cookie: str, hi_id) -> int:
        # 获取小说的付费章节号
        today_str = time.strftime("%Y-%m-%d", time.localtime())
    
        api = f"https://manage.hinw2a.com/BookRetention/bookDetail?book_id={hi_id}&date={today_str}%20-%20{today_str}&user_type=0"
        headers = {
            "Cookie": cookie
        }
        rsp = requests.get(api, headers=headers).text
        kadian = int(re.compile("付费章节: ?(\d+)").search(rsp).group(1))
        return kadian

    begin_cost_section_id = get_kadian(cookie, book_id)

    before_cost_num = df.loc[df["list_order"]==begin_cost_section_id-1, "current_chapter_users_total"].iloc[0]
    begin_cost_num = df.loc[df["list_order"]==begin_cost_section_id, "current_chapter_users_total"].iloc[0]
    
    try:
        zhuanhua = round(begin_cost_num / before_cost_num, 2)
    except:
        zhuanhua = 0.00
    
    df_readers_num = df[['list_order', 'current_chapter_users_total']].copy()
    df_readers_num.rename(columns={'list_order':'章节序号', 'current_chapter_users_total':'阅读人数'}, inplace=True)
    
    df_readers_num["是否免费"] = df_readers_num["章节序号"].apply(lambda x: 1 if x < begin_cost_section_id else 0)
    df_readers_num["章节流失阅读人数"] = df_readers_num["阅读人数"] - df_readers_num["阅读人数"].shift(1)
    df_readers_num["章节流失阅读人数"] = df_readers_num["章节流失阅读人数"].fillna(0).astype("int")
    df_readers_num["章节流失率"] = df_readers_num["章节流失阅读人数"] / df_readers_num["阅读人数"].shift(1)
    df_readers_num["章节流失率"] = df_readers_num["章节流失率"].fillna(0)
    df_readers_num["锁章章节号"] = begin_cost_section_id
    df_readers_num["锁章转化率"] = zhuanhua
    # 章节序号 - 阅读人数 - 是否免费 - 章节流失阅读人数 - 章节流失率 - 锁章章节号 - 锁章转化率
    return df_readers_num
