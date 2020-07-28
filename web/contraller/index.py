# -*- coding:utf-8 -*-
# author:fei2232
from flask import Blueprint,g
from common.libs.Helper import ops_render
from flask import Blueprint,request,redirect,jsonify
from common.libs.Helper import ops_render,iPagination,getCurrentDate,getUUID
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.models.Equip import WhiteoilEquip,WhiteoilPlatform,WhiteoilOil
from application import app, db
from sqlalchemy import or_
route_index = Blueprint('index_page',__name__)

@route_index.route("/")
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

    list = query.order_by(WhiteoilEquip.equip_id.desc()).all()[offset:limit]

    # 获取钻井平台信息
    platform_info = WhiteoilPlatform.query.with_entities(WhiteoilPlatform.platform_num,WhiteoilPlatform.platform_id).all()
    platform_info_dic = {}
    for p_id in platform_info:
        platform_info_dic[p_id[1]] = p_id[0]
    # 获取油品信息
    oil_info = WhiteoilOil.query.with_entities(WhiteoilOil.oil_name, WhiteoilOil.oil_id).all()
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