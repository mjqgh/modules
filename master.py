import requests
import pandas as pd


def h5_book_info(hn_id):
    # 用hinovel的小说id获取h5的小说信息，主要是h5的小说id以及卡点
    url_cookie = "https://raw.githubusercontent.com/mjqgh/modules/refs/heads/main/cookies.json"  # 从在线json中获取cookie
    dict_cookies = requests.get(url_cookie).json()
    cookie_h5 = dict_cookies["h5"]

    api = f"https://master-admin.thnovel.com/Book/getList?page=1&limit=100&book_source=-1&keyword={hn_id}&status=-1&h_status=-1&sign_type=-1&cost_type=-1&cate_id=-1&is_tweet=-1&update_date=&lang=en"
    headers = {
        "Cookie": cookie_h5,
        "X-Requested-With": "XMLHttpRequest"
    }
    rsp = requests.get(url=api, headers=headers).json()
    df = pd.DataFrame(rsp["data"]["items"])
    df_info = df.loc[df["book_id"]==hn_id, :].copy()
    # 卡点：init_charge_section
    # h5的小说id：id
    return df_info

def h5_edit_book_status(pid):
    # 批量审核小说上架
    edit_api = "http://aikan-admin.thnovel.com/Book/editBatchStatus"
    post_data = {
        "lang": "en",
        "status": 1,
        "product_list": json.dumps([{"productId":f"{pid}"},{"productId":""}]),
        "is_sync_status": 1
    }
    response = requests.post(edit_api, headers=self.headers, data=post_data).text
    return response

def h5_edit_book_price(h5_id, kadian, price_type=1, price=40):
    # 批量小说改价/改卡点
    # price_type：0=免费 1=千字 2=章节 (填充对应数字)
    # price：千字单价

    url_cookie = "https://raw.githubusercontent.com/mjqgh/modules/refs/heads/main/cookies.json"  # 从在线json中获取cookie
    dict_cookies = requests.get(url_cookie).json()
    cookie_h5 = dict_cookies["h5"]
    
    edit_api = "https://master-admin.thnovel.com/Book/editBatchPrice"
    post_data = {
        "lang": "en",
        "product_list": json.dumps([{"productId":f"{h5_id}","priceType":f"{price_type}","price":f"{price}","initiationChapter":f"{kadian}"}])
    }
    headers = {
        "Cookie": cookie_h5,
        "X-Requested-With": "XMLHttpRequest"
    }
    
    response = requests.post(edit_api, headers=headers, data=post_data).text
    return response
