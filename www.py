# -*- coding:utf-8 -*-
# author:fei2232
from application import app


# 统一拦截器
from web.interceptors.Authinterceptor import *
from web.interceptors.Errorinterceptor import *

# 蓝图功能，对所有的url进行蓝图功能配置

from web.contraller.index import route_index
from web.contraller.static import route_static
from web.contraller.user.User import route_user
from web.contraller.platform.Platform import route_platform
from web.contraller.equip.Equip import route_equip
from web.contraller.oil.Oil import route_oil
from web.contraller.account.Account import route_account


app.register_blueprint(route_index,url_prefix = "/")
app.register_blueprint(route_static,url_prefix = '/static')
app.register_blueprint(route_user,url_prefix = '/user')
app.register_blueprint(route_platform,url_prefix = '/platform')
app.register_blueprint(route_equip,url_prefix = '/equip')
app.register_blueprint(route_oil,url_prefix = '/oil')
app.register_blueprint(route_account,url_prefix = '/account')
