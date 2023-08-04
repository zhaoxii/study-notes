#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""易盾短信发送接口python示例代码
接口文档: http://dun.163.com/api.html
python版本：python2.7
说明文档：https://support.dun.163.com/documents/2018101001?docId=210168759616458752&locale=zh-cn#%E8%AF%B7%E6%B1%82%E5%85%AC%E5%85%B1%E5%8F%82%E6%95%B0
运行:
    1. 修改 SECRET_ID,SECRET_KEY,BUSINESS_ID 为对应申请到的值
    2. $ python smssend.py

"""
__author__ = 'yidun-dev'
__version__ = '0.1-dev'

from  hashlib import md5
import json
import random
import time
# import urllib
# import urllib.request
import  requests


class SmsSendAPIDemo(object):
    """易盾短信发送接口示例代码"""
    API_URL = "https://sms.dun.163.com/v2/sendsms"
    VERSION = "v2"

    def __init__(self, secret_id, secret_key, business_id):
        """
        Args:
            secret_id (str) 产品密钥ID，产品标识
            secret_key (str) 产品私有密钥，服务端生成签名信息使用
            business_id (str) 业务ID，易盾根据产品业务特点分配
        """
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.business_id = business_id

    def gen_signature(self, params=None):
        """生成签名信息
        Args:
            params (object) 请求参数
        Returns:
            参数签名md5值
        """
        buff = ""
        for k in sorted(params.keys()):
            buff += str(k) + str(params[k])
        buff += self.secret_key
        return md5(buff.encode("utf-8")).hexdigest()

    def send(self, params):
        params["secretId"] = self.secret_id
        params["businessId"] = self.business_id
        params["version"] = self.VERSION
        params["timestamp"] = int(time.time() * 1000)
        params["nonce"] = int(random.random() * 100000000)
        params["signature"] = self.gen_signature(params)

        try:
            # params = urllib.parse.urlencode(params)
            # params = params.encode('utf-8')
            # request = urllib.request.Request(self.API_URL, params)
            # content = urllib.request.urlopen(request, timeout=5).read()
            response=requests.post(self.API_URL,data=params)
            return response.json()
        except Exception as ex:
            print("调用API接口失败:", str(ex))


if __name__ == "__main__":
    """示例代码入口"""
    SECRET_ID = "a77f687582c280fe8fdbd8d364a25ebe"  # 产品密钥ID，产品标识
    SECRET_KEY = "aed71336ab9146066c6f41386a08c612"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
    BUSINESS_ID = "6bd15d1e4cbd4a38bf4f20914657addb"  # 业务ID，易盾根据产品业务特点分配
    api = SmsSendAPIDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)

    params = {
        "mobile": "15617135287",
        "templateId": "10084",
		"paramType": "json",
        "params": "{'a':'b'}"
    }
    ret = api.send(params)
    print(ret)
    if ret is not None:
        if ret["code"] == 200:
            taskId = ret["data"]["taskId"]
            print("taskId = %s" % taskId)
        else:
            print ("ERROR: ret.code=%s,msg=%s" % (ret['code'], ret['msg']))



