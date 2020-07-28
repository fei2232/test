# # coding: utf-8
# from sqlalchemy import Column, String
# from flask_sqlalchemy import SQLAlchemy
# from application import db
#
# class WhiteoilPlatform(db.Model):
#     __tablename__ = 'whiteoil_platform'
#
#     platform_id = db.Column(db.String(32), primary_key=True)
#     platform_province = db.Column(db.String(50))
#     platform_city = db.Column(db.String(50))
#     platform_country = db.Column(db.String(50))
#     platform_num = db.Column(db.String(50))
#     platform_status = db.Column(db.String(2))
#     platform_remark = db.Column(db.String(200))
