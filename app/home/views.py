# _*_ coding: utf-8 _*_
from . import home
from app import db
from app.models import User ,Goods,Orders,Cart,OrdersDetail
from flask import render_template, url_for, redirect, flash, session, request,make_response
from werkzeug.security import generate_password_hash
from functools import wraps
import random
import string
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO


def rndColor():
    '''随机颜色'''
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

def gene_text():
    '''生成4位验证码'''
    return ''.join(random.sample(string.ascii_letters+string.digits, 4))

def draw_lines(draw, num, width, height):
    '''划线'''
    for num in range(num):
        x1 = random.randint(0, width / 2)
        y1 = random.randint(0, height / 2)
        x2 = random.randint(0, width)
        y2 = random.randint(height / 2, height)
        draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

def get_verify_code():
    '''生成验证码图形'''
    code = gene_text()
    # 图片大小120×50
    width, height = 120, 50
    # 新图片对象
    im = Image.new('RGB',(width, height),'white')
    # 字体
    font = ImageFont.truetype('app/static/fonts/arial.ttf', 40)
    # draw对象
    draw = ImageDraw.Draw(im)
    # 绘制字符串
    for item in range(4):
        draw.text((5+random.randint(-3,3)+23*item, 5+random.randint(-3,3)),
                  text=code[item], fill=rndColor(),font=font )
    return im, code

@home.route('/code')
def get_code():
    image, code = get_verify_code()
    # 图片以二进制形式写入
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把buf_str作为response返回前端，并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    # 将验证码字符串储存在session中
    session['image'] = code
    return response

def user_login(f):
    """
    登录装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("home.login"))
        return f(*args, **kwargs)

    return decorated_function

@home.route("/collect_add/")
@user_login
def collect_add():
    """
    收藏景区
    """
    scenic_id = request.args.get("scenic_id", "")   # 接收传递的参数scenic_id
    user_id   = session.get('user_id',0)            # 获取当前用户的ID
    collect = Collect.query.filter_by(              # 根据用户ID和景区ID判断是否该收藏
        user_id =int(user_id),
        scenic_id=int(scenic_id)
    ).count()
    # 已收藏
    if collect == 1:
        data = dict(ok=0)     # 写入字典
    # 未收藏进行收藏
    if collect == 0:
        collect = Collect(
            user_id =int(user_id),
            scenic_id=int(scenic_id)
        )
        db.session.add(collect)  # 添加数据
        db.session.commit()      # 提交数据
        data = dict(ok=1)        # 写入字典
    import json                 # 导入模块
    return json.dumps(data)     # 返回json数据

@home.route("/collect_cancel/")
@user_login
def collect_cancel():
    """
    收藏景区
    """
    id = request.args.get("id", "")    # 获取景区ID
    user_id = session["user_id"]       # 获取当前用户ID
    collect = Collect.query.filter_by(id=id,user_id=user_id).first() # 查找Collect表，查看记录是否存在
    if collect :                      # 如果存在
        db.session.delete(collect)     # 删除数据
        db.session.commit()             # 提交数据
        data = dict(ok=1)               # 写入字典
    else :
        data = dict(ok=-1)           # 写入字典
    import json                     # 引入json模块
    return json.dumps(data)         # 输出json格式