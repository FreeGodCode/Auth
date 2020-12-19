# -*- coding: utf-8  -*-
# @Author: ty
# @File name: user.py 
# @IDE: PyCharm
# @Create time: 12/19/20 4:56 PM
from flask import render_template
from flask_login import login_required

# base_blueprint = Blueprint('base', __name__, url_prefix='/base')
from app import base_blueprint


@base_blueprint.route('/')
@login_required
def index():
    return render_template('index.html')


@base_blueprint.route('/north', methods=['POST'])
@login_required
def north():
    return render_template('layout/north.html')


@base_blueprint.route('/west', methods=['POST'])
@login_required
def west():
    return render_template('layout/west.html')


@base_blueprint.route('/south', methods=['POST'])
@login_required
def south():
    return render_template('layout/south.html')


@base_blueprint.route('/style/icons.jsp')
def icons():
    return render_template('icons/icons.html')

