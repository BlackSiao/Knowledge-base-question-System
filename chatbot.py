# -*- coding:utf-8 -*-
import hashlib
import base64
import hmac
import time
from urllib.parse import urlencode
import json
import websocket
import _thread as thread
import ssl
import gradio as gr

class Document_Q_And_A:
    def __init__(self, APPId, APISecret, TimeStamp, OriginUrl):
        self.appId = APPId
        self.apiSecret = APISecret
        self.timeStamp = TimeStamp
        self.originUrl = OriginUrl

    def get_origin_signature(self):
        m2 = hashlib.md5()
        data = bytes(self.appId + self.timeStamp, encoding="utf-8")
        m2.update(data)
        checkSum = m2.hexdigest()
        return checkSum



    def get_signature(self):
        # 获取原始签名
        signature_origin = self.get_origin_signature()
        # print(signature_origin)
        # 使用加密键加密文本
        signature = hmac.new(self.apiSecret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha1).digest()
        # base64密文编码
        signature = base64.b64encode(signature).decode(encoding='utf-8')
        # print(signature)
        return signature



    def get_header(self):
        signature = self.get_signature()
        header = {
            "Content-Type": "application/json",
            "appId": self.appId,
            "timestamp": self.timeStamp,
            "signature": signature
        }
        return header

    def get_url(self):
        signature = self.get_signature()
        header = {
            "appId": self.appId,
            "timestamp": self.timeStamp,
            "signature": signature
        }
        return self.originUrl + "?" + f'appId={self.appId}&timestamp={self.timeStamp}&signature={signature}'
        # 使用urlencode会导致签名乱码
        # return self.originUrl + "?" + urlencode(header)

    def get_body(self):
        data = {
            "chatExtends": {
                "wikiPromptTpl": "请将以下内容作为已知信息：\n<wikicontent>\n请根据以上内容回答用户的问题。\n问题:<wikiquestion>\n回答:",
                "wikiFilterScore": 65,
                "temperature": 0.5
            },
            "fileIds": [
                "0881b25e077c4318837b8dd61156dfb9" #上传文档后系统会返回一个fildId,此ID为独特值
            ],
            "messages": [
                {
                    "role": "user",
                    "content": "李火旺是主角吗？"
                },
                {
                    "role": "assistant",
                    "content": "李火旺是主角吗？"
                }
            ]
        }
        return data

# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws, close_status_code, close_msg):
    print("### closed ###")
    print("关闭代码：", close_status_code)
    print("关闭原因：", close_msg)


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(ws.question)
    ws.send(data)

# 收到websocket消息的处理
def on_message(ws, message):
    # print(message)
    data = json.loads(message)
    code = data['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        content = data["content"]
        status = data["status"]
        # print(f'status = {status}')
        print(content, end='')
        if status == 2:
            ws.close()
    return content

# 新的处理用户输入的函数
def get_answer(user_question):
    # 创建新的问题数据
    new_body = document_Q_And_A.get_body()
    new_body["messages"][0]["content"] = user_question
    new_body["messages"][1]["content"] = user_question

    # 获取新的 WebSocket 连接
    wsUrl = document_Q_And_A.get_url()
    headers = document_Q_And_A.get_header()
    body = new_body
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.appid = APPId
    ws.question = body

    # 运行 WebSocket 连接
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    return ws.content  # 假设 WebSocket 连接完成后，您可以获取内容

# 初始化文档问答系统
APPId = "455cbe1b"
APISecret = "OGU1NTM3MzU3MDgzYmZhZmU4MGQxY2Fl"
OriginUrl = "wss://chatdoc.xfyun.cn/openapi/chat"
curTime = str(int(time.time()))
document_Q_And_A = Document_Q_And_A(APPId, APISecret, curTime, OriginUrl)

# Gradio 的问答界面
iface = gr.Interface(
    fn=get_answer,  # 使用新的处理用户输入的函数
    inputs=gr.Textbox(),  # 使用文本框接收用户输入的问题
    outputs=gr.Textbox()  # 使用文本框显示模型的答案
)

# 启动 Gradio Web 服务
iface.launch()



if __name__ == '__main__':
    #初始化文档问答系统
    APPId = "455cbe1b"
    APISecret = "OGU1NTM3MzU3MDgzYmZhZmU4MGQxY2Fl"
    OriginUrl = "wss://chatdoc.xfyun.cn/openapi/chat"
    curTime = str(int(time.time()))
    document_Q_And_A = Document_Q_And_A(APPId, APISecret, curTime, OriginUrl)

    # Gradio 的问答界面
    iface = gr.Interface(
        fn=get_answer,  # 使用新的处理用户输入的函数
        inputs=gr.Textbox(),  # 使用文本框接收用户输入的问题
        outputs=gr.Textbox()  # 使用文本框显示模型的答案
    )

    # 启动 Gradio Web 服务
    iface.launch()
