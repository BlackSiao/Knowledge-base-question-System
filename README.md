# 本地知识问答系统

本项目基于讯飞星火大模型和 Gradio 生成的建议本地知识问答系统，提供了一个简单易用的 Web 交互界面。

## 准备工作

在运行项目之前，请完成以下准备工作：

1. 在讯飞星火大模型处开通 API，并开通关于知识库 API 的使用权限。获取 ID 和私钥：[讯飞云](https://www.xfyun.cn/)

2. 安装 Gradio：
   ```bash
   pip install gradio
   pip install requests_toolbelt
   
## 配置文件
在 Document_upload.py 中，根据你获得的 ID 和私钥，修改相应部分。运行 Document_upload.py 检查是否成功连接。若返回成功，复制返回的 fileID，并在其他代码中相应地修改 fileID 的部分。

运行项目
最终运行以下命令启动项目：

```bashbash
  python chatbot.py

对于错误码的提示，详情见官方对错误码的文档说明：https://www.xfyun.cn/doc/spark/ChatDoc-API.html#%E4%B8%80%E3%80%81%E6%9C%8D%E5%8A%A1%E4%BB%8B%E7%BB%8D

## 运行结果示例
![cover](./演示demo/demo2.png)


