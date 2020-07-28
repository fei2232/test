# -*- coding:utf-8 -*-
# author:fei2232
from flask import Blueprint,request,redirect,jsonify
from common.libs.Helper import ops_render,iPagination,getCurrentDate,getUUID
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.models.Equip import WhiteoilEquip,WhiteoilPlatform,WhiteoilOil
from application import app, db
from sqlalchemy import or_

route_equip = Blueprint( 'equip_page',__name__ )


@route_equip.route( "/index" )
def index():
    resp_data = {}
    req = request.values
    # 分页功能
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = WhiteoilEquip.query

    # 组合查询功能
    if 'mix_kw' in req:
        rule = or_(WhiteoilEquip.equip_platform.ilike("%{0}%".format(req['mix_kw'])), WhiteoilEquip.equip_id.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status'in req and (req['status']) != '-1':
        query = query.filter(WhiteoilEquip.equip_status == req['status'])


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

    list = query.order_by(WhiteoilEquip.equip_id).all()[offset:limit]
    # 获取钻井平台信息
    platform_info = WhiteoilPlatform.query.with_entities(WhiteoilPlatform.platform_num,WhiteoilPlatform.platform_id).all()
    platform_info_dic = {}
    for p_id in platform_info:
        platform_info_dic[p_id[1]] = p_id[0]
    # 获取油品信息
    oil_info = WhiteoilOil.query.with_entities(WhiteoilOil.oil_name,WhiteoilOil.oil_id).all()
    oil_info_dic = {}
    for o_id in oil_info:
        oil_info_dic[o_id[1]] = o_id[0]

    resp_data['list'] = list
    resp_data['platform_dic'] = platform_info_dic
    resp_data['oil_dic'] = oil_info_dic

    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render( "equip/index.html", resp_data)


@route_equip.route( "/set" ,methods = ["GET","POST"])
def set():
    if request.method =="GET":
        resp_data = {}
        platform_info_dic = {}
        oil_info_dic = {}
        req = request.args
        uid = req.get("id", 0)
        info = None
        if uid:
            info = WhiteoilEquip.query.filter_by(equip_id = uid).first()

        platform_info = WhiteoilPlatform.query.with_entities(WhiteoilPlatform.platform_num,WhiteoilPlatform.platform_id).all()
        if platform_info:
            for p_id in platform_info:
                platform_info_dic[p_id[1]] = p_id[0]

        oil_info = WhiteoilOil.query.with_entities(WhiteoilOil.oil_name,WhiteoilOil.oil_id).all()
        if oil_info:
            for o_id in oil_info:
                oil_info_dic[o_id[1]] = o_id[0]

        resp_data['info'] = info
        resp_data['platform_info'] = platform_info_dic
        resp_data['oil_info'] = oil_info_dic
        resp_data['search_con'] = req
        resp_data['status_mapping'] = app.config['STATUS_MAPPING']

        return ops_render( "equip/set.html", resp_data)

    resp = {'code':200,'msg':'操作成功！','data':{}}
    req = request.values

    equip_id = req['equip_id'] if 'equip_id' in req else 0
    equip_platform = req['equip_platform'] if 'equip_platform' in req else ''
    equip_oil = req['equip_oil'] if 'equip_oil' in req else ''

    equip_length = req['equip_length'] if 'equip_length' in req else ''
    equip_width = req['equip_width'] if 'equip_width' in req else ''
    equip_height = req['equip_height'] if 'equip_height' in req else ''
    equip_status = req['equip_status'] if 'equip_status' in req else ''
    equip_remark = req['equip_remark'] if 'equip_remark' in req else ''

    if equip_id is None or len(equip_id) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的设备编号！"
        return jsonify(resp)
    if equip_platform is None or len(equip_platform) <1:
        resp['code'] = -1
        resp['msg'] = "请选择所属钻井平台！"
        return jsonify(resp)
    if equip_oil is None or len(equip_oil) <1:
        resp['code'] = -1
        resp['msg'] = "请选择监测油品！"
        return jsonify(resp)
    if equip_length is None or len(equip_length) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的罐体长度！"
        return jsonify(resp)
    if equip_width is None or len(equip_width) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的罐体宽度！"
        return jsonify(resp)
    if equip_height is None or len(equip_height) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的罐体高度！"
        return jsonify(resp)
    if equip_status is None or len(equip_status) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的设备状态！"
        return jsonify(resp)
    if equip_remark is None or len(equip_remark) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的备注信息！"
        return jsonify(resp)

    has_in = WhiteoilEquip.query.filter(WhiteoilEquip.equip_id == equip_id).first()
    # 如果存在，则更新记录
    if has_in:
        has_in.equip_platform = equip_platform
        has_in.equip_oil = equip_oil
        has_in.equip_length = equip_length
        has_in.equip_width = equip_width
        has_in.equip_height = equip_height
        has_in.equip_status = equip_status
        has_in.equip_remark = equip_remark
        db.session.commit()
        return jsonify(resp)

@route_equip.route( "/add" ,methods = ["GET","POST"])
def add():
    if request.method =="GET":
        resp_data = {}
        platform_info_dic = {}
        oil_info_dic = {}
        req = request.args
        uid = req.get("id", 0)
        info = None
        if uid:
            info = WhiteoilEquip.query.filter_by(equip_id = uid).first()
        platform_info = WhiteoilPlatform.query.with_entities(WhiteoilPlatform.platform_num,WhiteoilPlatform.platform_id).all()
        if platform_info:
            for p_id in platform_info:
                platform_info_dic[p_id[1]] = p_id[0]

        oil_info = WhiteoilOil.query.with_entities(WhiteoilOil.oil_name, WhiteoilOil.oil_id).all()
        if oil_info:
            for o_id in oil_info:
                oil_info_dic[o_id[1]] = o_id[0]

        resp_data['info'] = info
        resp_data['platform_info'] = platform_info_dic
        resp_data['oil_info'] = oil_info_dic
        resp_data['search_con'] = req
        resp_data['status_mapping'] = app.config['STATUS_MAPPING']

        return ops_render( "equip/add.html", resp_data)

    resp = {'code':200,'msg':'操作成功！','data':{}}
    req = request.values

    equip_id = req['equip_id'] if 'equip_id' in req else ''
    equip_platform = req['equip_platform'] if 'equip_platform' in req else ''
    equip_oil = req['equip_oil'] if 'equip_oil' in req else ''
    equip_length = req['equip_length'] if 'equip_length' in req else ''
    equip_width = req['equip_width'] if 'equip_width' in req else ''
    equip_height = req['equip_height'] if 'equip_height' in req else ''
    equip_status = req['equip_status'] if 'equip_status' in req else ''
    equip_remark = req['equip_remark'] if 'equip_remark' in req else ''

    if equip_id is None or len(equip_id) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的设备编号！"
        return jsonify(resp)
    if equip_platform is None or len(equip_platform) <1:
        resp['code'] = -1
        resp['msg'] = "请选择所属钻井平台！"
        return jsonify(resp)
    if equip_oil is None or len(equip_oil) <1:
        resp['code'] = -1
        resp['msg'] = "请选择监测油品！"
        return jsonify(resp)
    if equip_length is None or len(equip_length) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的罐体长度！"
        return jsonify(resp)
    if equip_width is None or len(equip_width) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的罐体宽度！"
        return jsonify(resp)
    if equip_height is None or len(equip_height) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的罐体高度！"
        return jsonify(resp)
    if equip_status is None or len(equip_status) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的设备状态！"
        return jsonify(resp)
    if equip_remark is None or len(equip_remark) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的备注信息！"
        return jsonify(resp)

    # 新增记录
    has_in = WhiteoilEquip.query.filter(WhiteoilEquip.equip_id == equip_id).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = "该设备编号已存在！"
        return jsonify(resp)
    # 判断是否存在
    model_equip = WhiteoilEquip()
    model_equip.equip_id = equip_id
    model_equip.equip_platform = equip_platform
    model_equip.equip_oil = equip_oil
    model_equip.equip_length = equip_length
    model_equip.equip_width = equip_width
    model_equip.equip_height = equip_height
    model_equip.equip_status = equip_status
    model_equip.equip_remark = equip_remark

    db.session.add(model_equip)
    db.session.commit()
    return jsonify(resp)

@route_equip.route( "/ops" ,methods = ["POST"])
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

    equip_info = WhiteoilEquip.query.filter_by(equip_id=id).first()
    if not equip_info:
        resp['code'] = -1
        resp['msg'] = "指定记录不存在！"
        return jsonify(resp)

    if act == "remove":
        equip_info.equip_status = "0"
    elif act == "recover":
        equip_info.equip_status = "1"

    db.session.add(equip_info)
    db.session.commit()
    return jsonify(resp)