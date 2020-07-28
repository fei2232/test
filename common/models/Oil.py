# # coding: utf-8
# from sqlalchemy import Column, String
# from flask_sqlalchemy import SQLAlchemy
# from application import db
#
#
# class WhiteoilOil(db.Model):
#     __tablename__ = 'whiteoil_oil'
#
#     oil_id = db.Column(db.String(32), primary_key=True)
#     oil_name = db.Column(db.String(50))
#     oil_density = db.Column(db.Numeric(asdecimal=False))
#     oil_status = db.Column(db.String(2))
#     oil_remark = db.Column(db.String(200))
