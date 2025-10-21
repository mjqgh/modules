import requests
import pandas as pd


def pn_book_info(cookie, pn_id):
    # 获取pn小说的书籍信息
    url = f"http://aikan-admin.thnovel.com/Book/getList?page=1&limit=20&book_source=-1&keyword={pn_id}&status=-1&h_status=-1&sign_type=-1&cost_type=-1&cate_id=-1&is_tweet=-1&type=&update_date=&lang=en"
    headers = {
        "Cookie": cookie,
        "X-Requested-With": "XMLHttpRequest",
    }
    rsp = requests.get(url, headers=headers).json()
    # if rsp["data"]["total"] == 0:
    #     return None
    dict_rsp = rsp["data"]["items"][0]
    # init_charge_section 卡点锁章
    return dict_rsp

def book_chapter_data(cookie, pn_id, start, end):
    # 获取小说章节阅读数据
    def pn_book_kadian(cookie, pn_id):
        # 获取pn小说的书籍信息
        url = f"http://aikan-admin.thnovel.com/Book/getList?page=1&limit=20&book_source=-1&keyword={pn_id}&status=-1&h_status=-1&sign_type=-1&cost_type=-1&cate_id=-1&is_tweet=-1&type=&update_date=&lang=en"
        headers = {
            "Cookie": cookie,
            "X-Requested-With": "XMLHttpRequest",
        }
        rsp = requests.get(url, headers=headers).json()
        # if rsp["data"]["total"] == 0:
        #     return None
        dict_rsp = rsp["data"]["items"][0]
        # init_charge_section 卡点锁章
        return dict_rsp

    api = "http://aikan-admin.thnovel.com/BookStat/bookDayFullChapterStat"
    post_data = {
        "page": 1,
        "limit": 100,
        "order": "chapter_order asc",
        "date": f"{start} ~ {end}",
        "keyword": pn_id,
        "chapter_order": "",
        "lang": "en",
        "platform": "",
    }
    headers = {
        "Cookie": cookie,
        "X-Requested-With": "XMLHttpRequest",
    }

    rsp = requests.post(api, data=post_data, headers=headers).json()
    page_num = rsp["data"]["paging_data"]["total"] // 100 + 1

    df = pd.DataFrame(rsp["data"]["items"])
    for page in range(2, page_num + 1):
        print(f"Fetching page {page}/{page_num}...")
        post_data["page"] = page
        rsp2 = requests.post(api, data=post_data, headers=headers).json()
        df2 = pd.DataFrame(rsp2["data"]["items"])
        df = pd.concat([df, df2], ignore_index=True)

    df.sort_values("chapter_order", ascending=True, inplace=True)
    df = df.drop_duplicates(subset=["chapter_order"], keep='first', inplace=False)

    df["user_read_num"] = df["user_read_num"].astype(int)
    df["user_unlock_num"] = df["user_unlock_num"].astype(int)
    
    df["real_user_read_num"] = df["user_unlock_num"]
    df.loc[df["real_user_read_num"] == 0, "real_user_read_num"] = df.loc[df["real_user_read_num"] == 0, "user_read_num"]

    begin_cost_section_id = pn_book_kadian(cookie=cookie, pn_id=pn_id)["init_charge_section"]  # 获取锁章章节号
    df["if_free"] = df["chapter_order"].apply(lambda x: 1 if x < begin_cost_section_id else 0)

    df_readers_num = df[["chapter_order", "real_user_read_num", "if_free"]].copy()
    df_readers_num.rename(columns={"chapter_order": "章节序号", "real_user_read_num": "阅读人数", "if_free": "是否免费"}, inplace=True)

    df_readers_num["章节流失阅读人数"] = df_readers_num["阅读人数"] - df_readers_num["阅读人数"].shift(1)
    df_readers_num["章节流失阅读人数"] = df_readers_num["章节流失阅读人数"].fillna(0).astype("int")
    df_readers_num["章节流失率"] = df_readers_num["章节流失阅读人数"] / df_readers_num["阅读人数"].shift(1)
    df_readers_num["章节流失率"] = df_readers_num["章节流失率"].fillna(0)
    df_readers_num["锁章章节号"] = begin_cost_section_id

    before_lock_readers_num = df_readers_num.loc[df_readers_num["章节序号"] == begin_cost_section_id - 1, "阅读人数"].iloc[0]
    after_lock_readers_num = df_readers_num.loc[df_readers_num["章节序号"] == begin_cost_section_id, "阅读人数"].iloc[0]
    zhuanhua = after_lock_readers_num / before_lock_readers_num
    df_readers_num["锁章转化率"] = zhuanhua

    return df_readers_num

def adbook_roi(cookie, pn_id, start, end):
    # 获取投放书籍的ROI回收数据，周期总回款率
    api = f"http://aikan-admin.thnovel.com/AdCampaign/adRoiCollectList?page=1&limit=10&is_new_user=-1&create_user=&campaign_name={pn_id}&ad_platform=&platform=&lang=en&create_time={start}%20~%20{end}"
    headers = {
        "Cookie": cookie,
        "X-Requested-With": "XMLHttpRequest"
    }
    j_rsp = requests.get(api, headers=headers).json()
    dict_info = j_rsp_data = j_rsp['data']['items'][0]
    total_ad_fee = dict_info['total_ad_fee']
    total_pay_amount = dict_info['total_pay_amount']
    roi = total_pay_amount / total_ad_fee if total_ad_fee != 0 else None

    return [total_ad_fee, total_pay_amount, roi]
