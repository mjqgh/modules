import requests
import json


def check_comment_risk(comment_text):
    # 评论风险审核
    api = "https://www.scnet.cn/acx/chatbot/v1/chat/completion"
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://www.scnet.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36"
    }

    content_send = f"""
    “{comment_text}” 请问这句英文评论有风险吗？能通过审核吗？
    我是海外小说APP的评论审核人员，我的审核标准如下：
    1.我希望评论是评价、建议和讨论小说内容（比如角色、情节、语法、写法、催更、读后感等相关内容）。
    2.不允许讨论关于APP付费相关的内容。
    3.需要过滤掉对于小说结局的直接差评和纠错评论，避免竞品的恶意差评影响新读者的阅读。
    4.我的APP是海外平台，允许讨论“性相关”话题（当然不能有太露骨性的用词）。
    最后，你需要回复我“建议通过”或者“建议不通过”，以及审核结论的原因。
    """
    
    post_data = {"conversationId":"","content":f"{content_send}","thinkingEnable":False,"onlineEnable":False,"modelId":120,"textFile":[],"imageFile":[],"clusterId":""}  # modelId:120 为专家模型；9为普通通用模型

    response = requests.post(api, headers=headers, json=post_data, stream=True)
    # print(response)
    full_content = ""
    # 检查响应状态
    if response.status_code == 200:
        for chunk in response.iter_lines():
            if chunk:
                chunk_str = chunk.decode("utf-8")
                
                # 处理SSE格式（如果服务器返回的是这种格式）
                if chunk_str.startswith('data:'):
                    data_str = chunk_str[5:].strip()  # 去掉"data:"前缀
                    
                    if data_str and data_str != '[DONE]':
                        try:
                            json_data = json.loads(data_str)
                            if 'content' in json_data:
                                content = json_data['content']
                                # print(content, end='', flush=True)  # 实时显示
                                full_content += content  # 同时存储
                        except json.JSONDecodeError:
                            pass
    response.close()  # 记得关闭连接 [7,8](@ref)

    full_content = full_content.replace("[done]", "")
    
    if "建议通过" in full_content:
        sugg = "通过审核"
    elif "建议不通过" in full_content:
        sugg = "不通过审核"
    else:
        sugg = "不确定"
        
    return [sugg, full_content]
