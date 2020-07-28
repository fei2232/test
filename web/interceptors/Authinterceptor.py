# -*- coding:utf-8 -*-
# author:fei2232

from application import app
from flask import request,g,redirect
from common.models.User import WhiteoilUser
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
import re
# from common.libs.LogService import LogService

@app.before_request
def before_request():
    # 过滤url不需要登录验证
    ignore_urls = app.config['IGNORE_URLS']
    ignore_check_login_urls = app.config['IGNORE_CHECK_LOGIN_URLS']
    path = request.path

    pattern = re.compile('%s' % "|".join(ignore_check_login_urls))
    if pattern.match(path):
        return

    user_info = check_login()

    g.current_user = None

    if user_info:
        g.current_user = user_info

    # 加入日志   本项目不需要
    # LogService.addAccessLog()

    pattern = re.compile('%s' % "|".join(ignore_urls))
    if pattern.match(path):
        return

    if not user_info:
        return redirect(UrlManager.buildUrl("/user/login"))
    return


def check_login():
    cookies = request.cookies
    auth_cookie = cookies[app.config['AUTH_COOKIE_NAME']] if app.config['AUTH_COOKIE_NAME'] in cookies else ''
    if auth_cookie is None:
        return False
    auth_info = auth_cookie.split("#")
    if len(auth_info) !=2:
        return False
    try:
        use_info = WhiteoilUser.query.filter_by(user_id = auth_info[1]).first()
    except Exception:
        return False

    if use_info is None:
        return  False

    if auth_info[0] != UserService.geneAuthCode(use_info):
        return  False

    # 判断登录用户是否是可登录状态
    if use_info.user_status !="1":
        return False

    return use_info
