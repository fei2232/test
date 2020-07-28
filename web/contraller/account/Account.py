# -*- coding: utf-8 -*-
from flask import Blueprint,request,redirect,jsonify
from common.libs.Helper import ops_render,iPagination,getCurrentDate,getUUID
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.models.User import WhiteoilUser
from application import app, db
from sqlalchemy import or_

route_account = Blueprint( 'account_page',__name__ )

@route_account.route( "/index" )
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = WhiteoilUser.query

    if 'mix_kw' in req:
        rule = or_(WhiteoilUser.user_name.ilike("%{0}%".format(req['mix_kw'])), WhiteoilUser.user_pwd.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status'in req and (req['status']) != '-1':
        query = query.filter(WhiteoilUser.user_status == req['status'])


    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1)*app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE']*page

    list = query.order_by(WhiteoilUser.user_id.desc()).all()[offset:limit]

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render( "account/index.html", resp_data)

@route_account.route( "/set" ,methods = ["GET","POST"])
def set():
    default_pwd = "******"
    if request.method =="GET":
        resp_data = {}
        req = request.args
        uid = req.get("id", 0)
        info = None
        if uid:
            info = WhiteoilUser.query.filter_by(user_id = uid).first()

        resp_data['info'] = info
        resp_data['search_con'] = req
        resp_data['status_mapping'] = app.config['STATUS_MAPPING']

        return ops_render( "account/set.html", resp_data)


    resp = {'code':200,'msg':'操作成功！','data':{}}
    req = request.values

    user_id = req['user_id'] if 'user_id' in req else '0'

    user_name = req['user_name'] if 'user_name' in req else ''
    user_pwd = req['user_pwd'] if 'user_pwd' in req else ''
    user_status = req['user_status'] if 'user_status' in req else ''
    user_remark = req['user_remark'] if 'user_remark' in req else ''

    if user_name is None or len(user_name) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的用户名！"
        return jsonify(resp)
    if user_pwd is None or len(user_pwd) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的用户密码！"
        return jsonify(resp)
    if user_status is None or len(user_status) <1:
        resp['code'] = -1
        resp['msg'] = "请选择规范的用户状态！"
        return jsonify(resp)
    if user_remark is None or len(user_remark) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的备注信息！"
        return jsonify(resp)

    # 判断是否存在
    has_in = WhiteoilUser.query.filter(WhiteoilUser.user_name == user_name,WhiteoilUser.user_id != user_id).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = "该用户名已存在，请使用其他用户名！"
        return jsonify(resp)
    user_info = WhiteoilUser.query.filter_by(user_name = user_name).first()
    if user_info:
        model_user = user_info
    else:
        model_user = WhiteoilUser()
        model_user.user_id = getUUID()

    model_user.user_name = user_name
    model_user.user_status = user_status
    model_user.user_remark = user_remark
    if user_pwd != default_pwd:
        model_user.user_pwd = user_pwd

    db.session.add(model_user)
    db.session.commit()
    return jsonify(resp)

@route_account.route( "/ops" ,methods = ["POST"])
def ops():
    resp = {'code': 200, 'msg': '操作成功！', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号！"
        return jsonify(resp)
    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误请重试！"
        return jsonify(resp)

    user_info = WhiteoilUser.query.filter_by(user_id=id).first()
    if not user_info:
        resp['code'] = -1
        resp['msg'] = "指定用户不存在！"
        return jsonify(resp)

    if act == "remove":
        user_info.user_status = "0"
    elif act == "recover":
        user_info.user_status = "1"

    # user_info.update_time = getCurrentDate()
    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)
