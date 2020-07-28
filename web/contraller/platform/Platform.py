# -*- coding:utf-8 -*-
# author:fei2232
from flask import Blueprint,request,redirect,jsonify
from common.libs.Helper import ops_render,iPagination,getCurrentDate,getUUID
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.models.Equip import WhiteoilPlatform
from application import app, db
from sqlalchemy import or_

route_platform = Blueprint( 'platform_page',__name__ )


@route_platform.route( "/index" )
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = WhiteoilPlatform.query

    if 'mix_kw' in req:
        rule = or_(WhiteoilPlatform.platform_num.ilike("%{0}%".format(req['mix_kw'])), WhiteoilPlatform.platform_country.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status'in req and (req['status']) != '-1':
        query = query.filter(WhiteoilPlatform.platform_status == req['status'])


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

    list = query.order_by(WhiteoilPlatform.platform_id.desc()).all()[offset:limit]

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render( "platform/index.html", resp_data)

@route_platform.route( "/set" ,methods = ["GET","POST"])
def set():
    # default_pwd = "******"
    if request.method =="GET":
        resp_data = {}
        req = request.args
        uid = req.get("id", 0)
        info = None
        if uid:
            info = WhiteoilPlatform.query.filter_by(platform_id = uid).first()
        resp_data['info'] = info
        resp_data['search_con'] = req
        resp_data['status_mapping'] = app.config['STATUS_MAPPING']
        return ops_render( "platform/set.html", resp_data)


    resp = {'code':200,'msg':'操作成功！','data':{}}
    req = request.values

    platform_id = req['platform_id'] if 'platform_id' in req else '0'

    platform_province = req['platform_province'] if 'platform_province' in req else ''
    platform_city = req['platform_city'] if 'platform_city' in req else ''
    platform_country = req['platform_country'] if 'platform_country' in req else ''
    platform_num = req['platform_num'] if 'platform_num' in req else ''
    platform_status = req['platform_status'] if 'platform_status' in req else ''
    platform_remark = req['platform_remark'] if 'platform_remark' in req else ''

    if platform_province is None or len(platform_province) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的省份！"
        return jsonify(resp)
    if platform_city is None or len(platform_city) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的城市！"
        return jsonify(resp)
    if platform_country is None or len(platform_country) <1:
        resp['code'] = -1
        resp['msg'] = "请选择规范的区县！"
        return jsonify(resp)
    if platform_num is None or len(platform_num) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的编号！"
        return jsonify(resp)
    if platform_status is None or len(platform_status) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的平台状态！"
        return jsonify(resp)
    if platform_remark is None or len(platform_remark) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的备注信息！"
        return jsonify(resp)

    # 判断是否存在
    has_in = WhiteoilPlatform.query.filter(WhiteoilPlatform.platform_num == platform_num,WhiteoilPlatform.platform_id != platform_id).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = "该用户名已存在，请使用其他用户名！"
        return jsonify(resp)
    platform_info = WhiteoilPlatform.query.filter_by(platform_num = platform_num).first()
    if platform_info:
        model_platform = platform_info
    else:
        model_platform = WhiteoilPlatform()
        model_platform.platform_id = getUUID()

    model_platform.platform_province = platform_province
    model_platform.platform_city = platform_city
    model_platform.platform_country = platform_country
    model_platform.platform_num = platform_num
    model_platform.platform_status = platform_status
    model_platform.platform_remark = platform_remark

    db.session.add(model_platform)
    db.session.commit()
    return jsonify(resp)

@route_platform.route( "/ops" ,methods = ["POST"])
def ops():
    resp = {'code': 200, 'msg': '操作成功！', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的记录！"
        return jsonify(resp)
    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误请重试！"
        return jsonify(resp)

    platform_info = WhiteoilPlatform.query.filter_by(platform_id=id).first()
    if not platform_info:
        resp['code'] = -1
        resp['msg'] = "指定记录不存在！"
        return jsonify(resp)

    if act == "remove":
        platform_info.platform_status = "0"
    elif act == "recover":
        platform_info.platform_status = "1"

    # user_info.update_time = getCurrentDate()
    db.session.add(platform_info)
    db.session.commit()
    return jsonify(resp)