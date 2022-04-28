# _*_ coding:utf-8 _*_
from app import db
from . import admin
from flask import render_template, redirect, url_for, flash, session, request,jsonify
from app.models import Admin,Goods,SuperCat,SubCat,User,Orders,OrdersDetail
from sqlalchemy import or_
from functools import wraps
from decimal import *

def admin_login(f):
    """
    登录装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function

@admin.route("/goods/select_sub_cat/", methods=["GET"])
@admin_login
def select_sub_cat():
    """
    查找子分类
    """
    super_id = request.args.get("super_id", "")  # 接收传递的参数super_id
    subcat = SubCat.query.filter_by(super_cat_id = super_id).all()
    result = {}
    if subcat:
        data = []
        for item in subcat:
            data.append({'id':item.id,'cat_name':item.cat_name})
        result['status'] = 1
        result['message'] = 'ok'
        result['data'] = data
    else:
        result['status'] = 0
        result['message'] = 'error'
    return jsonify(result)   # 返回json数据
