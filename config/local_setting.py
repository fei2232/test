# -*- coding:utf-8 -*-
# author:fei2232
SERVER_PORT = 5500
DEBUG = True
SQLALCHEMY_ECHO = True
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@192.168.31.154/food_db'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:0nspeedcha@120.79.160.102/food_db'
SQLALCHEMY_DATABASE_URI = 'oracle+cx_oracle://WHITEOIL:WHITEOIL@120.79.160.102:1521/Ptecorcl'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = "utf-8"

AUTH_COOKIE_NAME = "whiteoil"

# 过滤Url
IGNORE_URLS = [
    "^/user/login"
]

IGNORE_CHECK_LOGIN_URLS = ["^/static",
                           "^/favicon.ico"
]

PAGE_SIZE = 50
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    "1":"启用",
    "0":"停用"
}

RELEASE_VERSION = "20180926"