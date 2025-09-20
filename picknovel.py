import requests
import pandas as pd
import re
import json


headers = {
    "Cookie": "PHPSESSID=5116f760b80ff5feb265e31833003d7f",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

headers_hinovel = {
    "Cookie": "PHPSESSID=80e1ec55f0c307f87bb9d7e4b2e13212",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

def hi_sync_pn(bids):
    # hi小说同步到picknovel
    # bid hi的小说ID，形如"38849,36749"
    sync_api = "https://manage.hinw2a.com/v3.OpenAuthorize/batchUpdate"
    post_data = {
        "book_id": bids,
        "status": 4
    }
    response = requests.post(sync_api, headers=headers_hinovel, data=post_data).text
    return response

def piliang_edit_book_status(pid):
    # 批量审核小说上架
    edit_api = "http://aikan-admin.thnovel.com/Book/editBatchStatus"
    post_data = {
        "lang": "en",
        "status": 1,
        "product_list": json.dumps([{"productId":f"{pid}"},{"productId":""}]),
        "is_sync_status": 1
    }
    response = requests.post(edit_api, headers=headers, data=post_data).text
    return response

def piliang_edit_book_price(pid, kadian, price_type=1, price=43):
    # 批量小说改价
    edit_api = "http://aikan-admin.thnovel.com/Book/editBatchPrice"
    post_data = {
        "lang": "en",
        "product_list": json.dumps([{"productId":f"{pid}","priceType":f"{price_type}","price":f"{price}","initiationChapter":f"{kadian}"}])
    }
    response = requests.post(edit_api, headers=headers, data=post_data).text
    return response

def search_pn_id(bid):
    # 用hi的ID查询pn的小说ID，如果是待审核则改为上架，并且改价
    # bid hi的小说ID
    search_api = f"http://aikan-admin.thnovel.com/Book/getList?page=1&limit=20&keyword={bid}&lang=en"
    response = requests.get(search_api, headers=headers).json()
    items = response['data']['items']
    if len(items) == 0:
        pn_id = 0 # 没有找到
    else:
        for item in items: # 可能有多个结果，需要匹配hi的ID
            book_id = item['book_id']
            kadian = item["init_charge_section"]
            book_status = item['book_status']  # 待审核/已完结
            if (book_id == bid) and ("待审核" not in book_status):  # 找到并且不是待审核
                pn_id = item['id']
                break
            elif (book_id == bid) and ("待审核" in book_status):  # 找到但是待审核
                pn_id = item['id']
                piliang_edit_book_status(pn_id)  # 批量修改小说状态
                piliang_edit_book_price(pid=pn_id, kadian=kadian, price=43)  # 批量修改小说价格
                break
            else:
                pn_id = 0 # 没有找到
    return pn_id

def get_column_info(column_id, group_type=1):
    # 获取栏目全部小说（包括上架和下架）
    # recommend_category_id=4 热门搜索
    api = "http://aikan-admin.thnovel.com/HomeRecommendProduct/getList"
    params = {
        "page": "1",
        "limit": "20000",
        "type": "1",
        "group_type": group_type,  # 1 栏目 2 搜索
        "name": "",
        "status": "-1",
        "lang": "en",
        "tab_type": "-1",
        "recommend_category_id": column_id
    }
    response = requests.get(api, params=params, headers=headers).text
    json_data = json.loads(response)
    data = json_data['data']['items']
    df = pd.DataFrame(data)
    return df
    # id 房间号
    # product_id PN的小说ID
    # status 0上架 1下架

def edit_book(cid, pid, status=0, order=1, hot=0, rid=0, lang="en"):
    # 编辑栏目小说(新增或修改)
    # cid 栏目ID
    # pid PN的小说ID
    # status 0上架 1下架
    # order 数字越小越靠前
    # hot 1 热门 0 非热门
    # rid id 房间号，为0表示新增
    # lang 语言
    edit_api = "http://aikan-admin.thnovel.com/HomeRecommendProduct/editData"
    post_data = {
        "type": 1,
        "recommend_category_id": cid,  # 栏目ID
        # "product_name": "40423 -  (The Giants & Sex Slaved Virgins)",
        "product_id": pid,  # PN的小说ID
        "list_order": order,  # 数字越小越靠前
        "is_hot": hot,  # 1 热门 0 非热门
        "status": status,  # 0上架 1下架
        "id": rid,  # id 房间号，为0表示新增
        "lang": lang,  # 语言
    }
    response = requests.post(edit_api, headers=headers, data=post_data).text
    # print(response)
    return response