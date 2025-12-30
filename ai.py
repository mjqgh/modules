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
    1.我希望评论是评价、建议和讨论小说内容（比如角色、情节、语法、写法、读后感、合理推测、表达喜爱的表情符号等相关内容）。
    2.禁止支付与定价讨论：禁止任何关于APP付费、章节定价、充值方式、性价比抱怨等与交易相关的内容。
    3.需要过滤掉对于小说结局的直接差评，避免竞品的恶意差评影响新读者的阅读。
    4.有纠错的评论一律不通过审核（涉及内容重复的也属于纠错），APP会自动同步给作者确认，无需通过审核，避免影响其他读者判断。
    5.允许讨论提及“性相关”情节或主题，但禁止露骨、直白的情色描写、挑逗性言论，或纯粹寻求色情内容的诱导性提问。
    6.允许表达对更多内容的期待或鼓励性催更，但禁止抱怨更新缓慢或变相讽刺作品未完结的言论。
    7.禁止阅读体验与技术问题反馈：禁止发布与APP使用体验、技术故障、个人网络或设备问题相关的评论。
    8.除了提及我们自己APP“Hinovel”，不能提及其他任何互联网产品的名字，提及就一律不通过，即使是一条好评论。

    最后，如果建议通过，回复我暗号“通过666”；如果建议不通过，回复我暗号“拒绝886”；此外，还要回复审核结论的原因。
    """
    
    post_data = {"conversationId":"","content":f"{content_send}","thinkingEnable":False,"onlineEnable":False,"modelId":120,"textFile":[],"imageFile":[],"clusterId":""}

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

    if "通过666" in full_content:
        sugg = "通过审核"
    elif "拒绝886" in full_content:
        sugg = "不通过审核"
    else:
        sugg = "不确定"
        
    return [sugg, full_content]
