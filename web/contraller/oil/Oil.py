# -*- coding:utf-8 -*-
# author:fei2232
from flask import Blueprint,request,redirect,jsonify
from common.libs.Helper import ops_render,iPagination,getCurrentDate,getUUID
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.models.Equip import WhiteoilOil
from application import app, db
from sqlalchemy import or_

route_oil = Blueprint( 'oil_page',__name__ )


@route_oil.route( "/index" )
def index():
    resp_data = {}
    req = request.values
    # 分页功能
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = WhiteoilOil.query

    # 组合查询功能
    if 'mix_kw' in req:
        rule = or_(WhiteoilOil.oil_name.ilike("%{0}%".format(req['mix_kw'])), WhiteoilOil.oil_density.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status'in req and (req['status']) != '-1':
        query = query.filter(WhiteoilOil.oil_status == req['status'])


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

    list = query.order_by(WhiteoilOil.oil_name).all()[offset:limit]

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render( "oil/index.html", resp_data)


@route_oil.route( "/set" ,methods = ["GET","POST"])
def set():

    if request.method =="GET":
        resp_data = {}
        req = request.args
        uid = req.get("id", 0)
        info = None
        if uid:
            info = WhiteoilOil.query.filter_by(oil_id = uid).first()
        resp_data['info'] = info

        resp_data['search_con'] = req
        resp_data['status_mapping'] = app.config['STATUS_MAPPING']

        return ops_render( "oil/set.html", resp_data)


    resp = {'code':200,'msg':'操作成功！','data':{}}
    req = request.values

    oil_id = req['oil_id'] if 'oil_id' in req else '0'

    oil_name = req['oil_name'] if 'oil_name' in req else ''
    oil_density = req['oil_density'] if 'oil_density' in req else ''
    oil_status = req['oil_status'] if 'oil_status' in req else ''
    oil_remark = req['oil_remark'] if 'oil_remark' in req else ''

    if oil_name is None or len(oil_name) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的油品名！"
        return jsonify(resp)
    if oil_density is None or len(oil_density) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的油品密度！"
        return jsonify(resp)
    if oil_status is None or len(oil_status) <1:
        resp['code'] = -1
        resp['msg'] = "请选择规范的油品状态！"
        return jsonify(resp)
    if oil_remark is None or len(oil_remark) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的备注信息！"
        return jsonify(resp)

    # 判断是否存在
    has_in = WhiteoilOil.query.filter(WhiteoilOil.oil_name == oil_name,WhiteoilOil.oil_id != oil_id).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = "该油品名已存在，请使用其他油品名！"
        return jsonify(resp)
    oil_info = WhiteoilOil.query.filter_by(oil_id = oil_id).first()
    if oil_info:
        model_oil = oil_info
    else:
        model_oil = WhiteoilOil()
        model_oil.oil_id = getUUID()

    model_oil.oil_name = oil_name
    model_oil.oil_density = oil_density
    model_oil.oil_status = oil_status
    model_oil.oil_remark = oil_remark

    db.session.add(model_oil)
    db.session.commit()
    return jsonify(resp)

@route_oil.route( "/ops" ,methods = ["POST"])
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

    oil_info = WhiteoilOil.query.filter_by(oil_id=id).first()
    if not oil_info:
        resp['code'] = -1
        resp['msg'] = "指定记录不存在！"
        return jsonify(resp)

    if act == "remove":
        oil_info.oil_status = "0"
    elif act == "recover":
        oil_info.oil_status = "1"

    db.session.add(oil_info)
    db.session.commit()
    return jsonify(resp)
