# -*- coding:utf-8 -*-
# author:fei2232

from application import app
from common.libs.Helper import ops_render
# from common.libs.LogService import LogService

@app.errorhandler(404)
def error_404(e):
    # 写日志  本项目不需要
    # LogService.addErrorLog(str(e))

    return ops_render('error/error.html', {'status': 404, 'msg': '很抱歉，您访问的页面不存在！'})