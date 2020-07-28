# -*- coding:utf-8 -*-
# author:fei2232
##公用配置
SERVER_PORT = 9090
DEBUG = False
SQLALCHEMY_ECHO = False

# AUTH_COOKIE_NAME = "mooc_food"

# 过滤Url
IGNORE_URLS = [
    "^/user/login"
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]