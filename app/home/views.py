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