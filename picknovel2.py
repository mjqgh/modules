import requests


def pn_book_info(cookie, pn_id):
    url = f"http://aikan-admin.thnovel.com/Book/getList?page=1&limit=20&book_source=-1&keyword={pn_id}&status=-1&h_status=-1&sign_type=-1&cost_type=-1&cate_id=-1&is_tweet=-1&type=&update_date=&lang=en"
    headers = {
        "Cookie": cookie,
        "X-Requested-With": "XMLHttpRequest",
    }
    rsp = requests.get(url, headers=headers).json()
    if rsp["data"]["total"] == 0:
        return None
    dict_rsp = rsp["data"]["items"][0]
    # init_charge_section 卡点锁章
    return dict_rsp
