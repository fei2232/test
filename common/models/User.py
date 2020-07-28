# coding: utf-8
from sqlalchemy import Column, String
from flask_sqlalchemy import SQLAlchemy
from application import db


class WhiteoilUser(db.Model):
    __tablename__ = 'whiteoil_user'

    user_id = db.Column(db.String(32), primary_key=True)
    user_name = db.Column(db.String(50), unique=True)
    user_pwd = db.Column(db.String(50))
    user_status = db.Column(db.String(2))
    user_remark = db.Column(db.String(200))