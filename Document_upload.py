# -*- coding:utf-8 -*-
import hashlib
import base64
import hmac
import time
import random
from urllib.parse import urlencode
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

class Document_Upload:
    def __init__(self, APPId, APISecret, timestamp):
        self.APPId = APPId
        self.APISecret = APISecret
        self.Timestamp = timestamp

    def get_origin_signature(self):
        m2 = hashlib.md5()
        data = bytes(self.APPId + self.Timestamp, encoding="utf-8")
        m2.update(data)
        checkSum = m2.hexdigest()
        return checkSum


    def get_signature(self):
        # 获取原始签名
        signature_origin = self.get_origin_signature()
        # 使用加密键加密文本
        signature = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha1).digest()
        # base64密文编码
        signature = base64.b64encode(signature).decode(encoding='utf-8')
        return signature

    def get_header(self):
        signature = self.get_signature()
        header = {
            "appId": self.APPId,
            "timestamp": self.Timestamp,
            "signature": signature,
        }
        return header

    # 提交网络文件
    def get_body(self):
        body = {
            "file": "",
            "url": "http://xingh.dsd.xss/e-0867bed7d1a3/c5a58172-8c1c-4c79-90e0-de4042ba876d1691741866951.txt",
            "fileName": "c5a58112313876d1691741866951.txt",
            "fileType": "wiki",
            "callbackUrl": "your_callbackUrl"
        }
        form = MultipartEncoder(
            fields=body,
            boundary='------------------' + str(random.randint(1e28, 1e29 - 1))
        )
        return form

    # 提交本地文件
    def get_files_and_body(self):
        body = {
            "url": "",
            "fileName": "背影.txt",
            "fileType": "wiki",     #目前文件类型固定为wiki
            "needSummary": False,   #设置不对文档进行总结
            "stepByStep": False,
            "callbackUrl": "your_callbackUrl",
        }
        files = {'file': open('背影.txt', 'rb')}  #rb表示二进制读取 ？？？是不是这里有问题？
        return files, body

if __name__ == '__main__':
    APPId = "455cbe1b"
    APISecret = "OGU1NTM3MzU3MDgzYmZhZmU4MGQxY2Fl"
    curTime = str(int(time.time()))
    request_url = "https://chatdoc.xfyun.cn/openapi/fileUpload"

    document_upload = Document_Upload(APPId, APISecret, curTime)
    headers = document_upload.get_header()

    # ******************提交网络文件
    # body = document_upload.get_body()
    # headers['Content-Type'] = body.content_type
    # response = requests.post(request_url, data=body, headers=headers)

    # ******************提交本地文件
    files, body = document_upload.get_files_and_body()
    response = requests.post(request_url, files=files, data=body, headers=headers)

    print("请求头", response.request.headers, type(response.request.headers))
    print('onMessage：\n' + response.text)

    # 文档上传成功
