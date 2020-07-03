# -*- coding: utf-8 -*-

import time
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import os
#需要填写你的 Access Key 和 Secret Key
access_key = 'JU3KZ9p75Dfcjprt0O9HfUpKEFsea_Liwf6KV0wE' #这里的密钥填上刚才我让你记住的密钥对
secret_key = 'OdsrnZZYO1lUFX7eiNG6YSM0w8ADRulapyOUcCTR' #这里的密钥填上刚才我让你记住的密钥对

#构建鉴权对象
q = Auth(access_key, secret_key)

#要上传的空间
bucket_name = 'jinwanchishenme'

#上传到七牛后保存的文件名
key = '%s_%s_%s_%s_%s_%s.jpg'%(time.localtime()[0],time.localtime()[1],time.localtime()[2],time.localtime()[3],time.localtime()[4],time.localtime()[5])

#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)

#要上传文件的本地路径
localfile = 'current_photo.jpg'

ret, info = put_file(token, key, localfile)

filename = 'current_photo.jpg'
if os.path.exists(filename):
    os.remove(filename)