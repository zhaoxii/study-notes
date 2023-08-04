import os
import random

from flask import session
from qiniu import Auth, put_file, etag, put_data
import qiniu.config

from apps.artical.model import Article_type
from apps.user.model import User
from config import Config
from qiniu import BucketManager

# 需要填写你的 Access Key 和 Secret Key
def upload_qiniu(filestorage):
    access_key = 'G7iR1derRI3Q1b35wz9IUoyD-hf0qRtfPm68hNoP'
    secret_key = 'xSpKtqyGXlE10EB27vbA6zmZW-JYXY5_IE1bVa_i'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'mmmmmmyyblog'

    # 上传后保存的文件名
    filename = filestorage.filename
    rand=random.randint(1,1000)
    suffix=filename.rsplit('.')[-1]
    key = filename.rsplit('.')[0] + '_' + str(rand) + '.' + suffix   # 文件名

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径
    # localfile = ''
    # ret, info = put_file(token, key, localfile, version='v2')
    ret,info=put_data(token,key,filestorage.read())   # filestorage.read() 将图片以 二进制读出来
    return ret,info



def del_qiniu(filename):
    access_key = 'G7iR1derRI3Q1b35wz9IUoyD-hf0qRtfPm68hNoP'
    secret_key = 'xSpKtqyGXlE10EB27vbA6zmZW-JYXY5_IE1bVa_i'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    #初始化BucketManager
    bucket = BucketManager(q)

    #你要测试的空间， 并且这个key在你空间中存在
    bucket_name = 'mmmmmmyyblog'
    key = filename   # 图片名

    #删除bucket_name 中的文件 key
    ret, info = bucket.delete(bucket_name, key)
    return info


def user_type():
    # 获取文章分类
    types = Article_type.query.all()
    # 登录用户
    user = None
    user_id = session.get('uid', None)
    if user_id:
        user = User.query.get(user_id)
    return user, types


