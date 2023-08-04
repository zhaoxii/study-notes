# -*- coding: utf-8 -*-
# flake8: noqa
import os

from qiniu import Auth
from qiniu import BucketManager
from qiniu import Auth, put_file, etag
import qiniu.config

#需要填写你的 Access Key 和 Secret Key
from config import Config

# access_key = 'G7iR1derRI3Q1b35wz9IUoyD-hf0qRtfPm68hNoP'
# secret_key = 'xSpKtqyGXlE10EB27vbA6zmZW-JYXY5_IE1bVa_i'
#
# #构建鉴权对象
# q = Auth(access_key, secret_key)
#
# #要上传的空间
# bucket_name = 'myyyyyflaskblog'
#
# #上传后保存的文件名
# key = '007.png'
#
# #生成上传 Token，可以指定过期时间等
# token = q.upload_token(bucket_name, key, 3600)
#
# #要上传文件的本地路径
# localfile = os.path.join(Config.UPLOAD_ICON_DIR,'QQ20211005154310.png')
#
# ret, info = put_file(token, key, localfile, version='v2')
# print(info)
# print(ret)
# #    _ResponseInfo__response:<Response [200]>, exception:None, status_code:200, text_body:{"hash":"FqIKeFInKfRlCdeiT2WAfBLRiNeh","key":"my-python-logo.png"}, req_id:M2QAAACNw0tZZ80W, x_log:X-Log
# #    {'hash': 'FqIKeFInKfRlCdeiT2WAfBLRiNeh', 'key': 'my-python-logo.png'}
#
# print(info.status_code)  # 200
# print(info.text_body)  # text_body 是一个字符串，不是一个字典 。 内容与ret的相同








# access_key = 'G7iR1derRI3Q1b35wz9IUoyD-hf0qRtfPm68hNoP'
# secret_key = 'xSpKtqyGXlE10EB27vbA6zmZW-JYXY5_IE1bVa_i'
#
# #初始化Auth状态
# q = Auth(access_key, secret_key)
#
# #初始化BucketManager
# bucket = BucketManager(q)
#
# #你要测试的空间， 并且这个key在你空间中存在
# bucket_name = 'myyyyyflaskblog'
# key = 'my-python-logo.png'
#
# #获取文件的状态信息
# ret, info = bucket.delete(bucket_name, key)   # _ResponseInfo__response:<Response [200]>, exception:None, status_code:200, text_body:, req_id:lY0AAADrQYRvc80W, lY0AAADrQYRvc80W, x_log:-
#
# print(info)
# print(ret)





