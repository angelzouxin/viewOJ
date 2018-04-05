import configparser
import os
import json
import requests


class WeChatAlarms:

    def __init__(self):
        cf = configparser.ConfigParser()
        config_file_path = os.path.join(os.path.dirname(__file__), "../../wechat_token.ini")
        cf.read(config_file_path)
        self.CorpId = cf.get('wechat', 'CropId')
        self.AgentId = cf.get('wechat', 'AgentId')
        self.Secret = cf.get('wechat', 'Secret')

    def get_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {
           'corpid': self.CorpId,
           'corpsecret': self.Secret,
          }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def send_msg(self, msg):
        url = ("https://qyapi.weixin.qq.com/cgi-bin/message/send"
               "?access_token={}").format(self.get_token())
        values = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": self.AgentId,
            "text": {
               "content": msg
            },
        }

        req = requests.post(url, json.dumps(values))
        print(values, req)
