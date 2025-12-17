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

    post_data = {"conversationId":"","content":f"“{comment_text}” 这句英文评论有风险吗？能通过审核吗？我希望评论是评价、建议和讨论小说内容（比如角色、情节、语法、写法、催更等相关内容），特别是讨论关于APP付费相关的一律不通过，最后你需要回复我“建议通过”或者“建议不通过”，以及审核结论的原因","thinkingEnable":False,"onlineEnable":False,"modelId":9,"textFile":[],"imageFile":[],"clusterId":""}

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
                                print(content, end='', flush=True)  # 实时显示
                                full_content += content  # 同时存储
                        except json.JSONDecodeError:
                            pass
    
    response.close()  # 记得关闭连接 [7,8](@ref)
    
    return full_content
