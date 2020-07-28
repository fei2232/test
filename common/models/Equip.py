# coding: utf-8
from sqlalchemy import Column, String
from flask_sqlalchemy import SQLAlchemy
from application import db
# from common.models.Platform import WhiteoilPlatform

class WhiteoilEquip(db.Model):
    __tablename__ = 'whiteoil_equip'

    equip_id = db.Column(db.String(32), primary_key=True)
    equip_platform = db.Column(db.ForeignKey('whiteoil_platform.platform_id'))
    equip_oil = db.Column(db.ForeignKey('whiteoil_oil.oil_id'))
    equip_length = db.Column(db.Numeric(asdecimal=False))
    equip_width = db.Column(db.Numeric(asdecimal=False))
    equip_height = db.Column(db.Numeric(asdecimal=False))
    equip_status = db.Column(db.String(2))
    equip_remark = db.Column(db.String(200))

    whiteoil_oil = db.relationship('WhiteoilOil', primaryjoin='WhiteoilEquip.equip_oil == WhiteoilOil.oil_id', backref='whiteoil_equips')
    whiteoil_platform = db.relationship('WhiteoilPlatform', primaryjoin='WhiteoilEquip.equip_platform == WhiteoilPlatform.platform_id', backref='whiteoil_equips')


class WhiteoilOil(db.Model):
    __tablename__ = 'whiteoil_oil'

    oil_id = db.Column(db.String(32), primary_key=True)
    oil_name = db.Column(db.String(50))
    oil_density = db.Column(db.Numeric(asdecimal=False))
    oil_status = db.Column(db.String(2))
    oil_remark = db.Column(db.String(200))


class WhiteoilPlatform(db.Model):
    __tablename__ = 'whiteoil_platform'

    platform_id = db.Column(db.String(32), primary_key=True)
    platform_province = db.Column(db.String(50))
    platform_city = db.Column(db.String(50))
    platform_country = db.Column(db.String(50))
    platform_num = db.Column(db.String(50))
    platform_status = db.Column(db.String(2))
    platform_remark = db.Column(db.String(200))
