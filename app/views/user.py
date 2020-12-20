# -*- coding: utf-8  -*-
# @Author: ty
# @File name: user.py 
# @IDE: PyCharm
# @Create time: 12/19/20 4:56 PM
import hashlib
import uuid
from datetime import datetime

from flask import render_template, request, jsonify
from flask_login import logout_user, login_user

from app import base_blueprint, db
from app.models.Organization import Organization
from app.models.Role import Role
from app.models.User import User


@base_blueprint.route('user/login', methods=['GET'])
def user_login():
    """
    登录
    :return:
    """
    return render_template('user/login.html')


@base_blueprint.route('/user/form', methods=['GET'])
def user_form():
    """

    :return:
    """
    return render_template('user/form.html', id=request.args.get('id', ''))


@base_blueprint.route('/user/grant_user_organization', methods=['GET'])
def grant_user_organization_page():
    """

    :return:
    """
    return render_template('user/grant_user_organization.html', id=request.args.get('id', ''))


@base_blueprint.route('/user/grant_user_role', methods=['GET'])
def grant_user_role_page():
    """

    :return:
    """
    return render_template("user/grant_user_role.html", id=request.args.get('id', ''))


@base_blueprint.route('/user/organization', methods=['POST'])
def grant_user_organization():
    """

    :return:
    """
    id = request.form.get('id', '')
    ids = request.form.get('ids', '')
    # user = User.query.get(id)
    user = db.session.query(User).get(id)

    if not ids:
        user.organizations = []
    else:
        id_list = ids.split(',')
        user.organizations = [Organization.query.get(o_id) for o_id in id_list]

    db.session.add(user)
    return jsonify({'success': True})


@base_blueprint.route('/user/grant_user_role', methods=['POST'])
def grant_user_role():
    """

    :return:
    """
    id = request.form.get('id', '')
    ids = request.form.get('ids', '')

    # user = User.query.get(id)
    user = db.session.query(User).get(id)
    if not ids:
        user.roles = []
    else:
        id_list = ids.split(',')
        user.roles = [Role.query.get(r_id) for r_id in id_list]

    db.session.add(user)
    return jsonify({'success': True})


@base_blueprint.route('/user/do_logout', methods=['POST'])
def do_logout():
    logout_user()
    return jsonify({'success': True})


@base_blueprint.route('/user/do_login', methods=['POST'])
def do_login():
    """

    :return:
    """
    # 检查用户是否存在
    user = User.query.filter_by(nickname=request.form['data.nickname']).first()
    if user:
        # 密码进行MD5加密
        md = hashlib.md5()
        md.update(request.form['data.pwd'].encode('utf-8'))
        # encoded_pwd = md.update(request.form['data.pwd'].encode('utf-8')).hexdigest()
        # 加密后的密码和数据库中的密码进行比较
        # if encoded_pwd == user.password:
        if md.hexdigest() == user.password:
            login_user(user)
            return jsonify({'success': True, 'msg': ''})
    return jsonify({'success': False, 'msg': 'password error'})


@base_blueprint.route('/user/', methods=['GET'])
def user_index():
    """

    :return:
    """
    return render_template('user/index.html')


@base_blueprint.route('/user_grid', methods=['POST'])
def user_grid():
    """

    :return:
    """
    page = request.form.get('page', 1, type=int)
    nums = request.form.get('nums', 10, type=int)
    pagination = User.query.paginate(page, per_page=nums, error_out=False)
    users = pagination.items
    return jsonify([user.to_join() for user in users])


@base_blueprint.route('/user/get_user_by_id', methods=['POST'])
def get_user_by_id():
    """

    :return:
    """
    # user = User.query.get(request.form.get('id'))
    user = db.session.query(User).get(request.form.get('id'))
    if user:
        return jsonify(user.to_join)
    # return jsonify({'success': False, 'msg': 'error' })
    return jsonify({'code': 400, 'msg': 'error'})


@base_blueprint.route('/user/update', methods=['POST'])
def user_update():
    """

    :return:
    """
    id = request.form.get('data.id', '')
    nickname = request.form.get('data.nickname', '')
    if User.query.filter(User.nickname == nickname).filter(User.id != id).first():
        return jsonify({'success': False, 'msg': '更新用户失败,用户名已存在'})

    user = db.session.query(User).get(id)
    # user = User.query.get(id)
    user.nickname = request.form.get('data.nickname', '')
    user.name = request.form.get('data.name', '')
    user.sex = request.form.get('data.sex', '')
    user.age = request.form.get('data.age', '')
    user.img = request.form.get('data.img', '')
    user.update_time = datetime.now()

    db.session.add(user)
    # return jsonify({'success': True, 'msg': '更新成功'})
    return jsonify({'code': 200, 'msg': '更新成功'})


@base_blueprint.route('/user/save', methods=['POST'])
def user_save():
    """

    :return:
    """
    if User.query.filter_by(nickname=request.form.get('data.nickname')).first():
        return jsonify({'success': False, 'msg': '用户已存在'})

    user = User()
    user.id = str(uuid.uuid4())

    md = hashlib.md5()
    md.update('123456'.encode('utf-8'))
    user.password = md.hexdigest()
    # user.password = hashlib.md5().update('123456'.encode('utf-8')).hexdigest()
    user.name = request.form.get('data.name')
    user.nickname = request.form.get('data.nickname')
    user.sex = request.form.get('data.sex')
    user.age = request.form.get('data.age')
    user.img = request.form.get('data.img')

    db.session.add(user)
    # return jsonify({"success": True, 'msg': '新建用户成功,默认密码为:123456'})
    return jsonify({"code": 200, 'msg': '新建用户成功,默认密码为:123456'})


@base_blueprint.route('/user/delete', methods=['POST'])
def user_delete():
    # user = User.query.get(request.form.get('id'))
    user = db.session.query(User).get(request.form.get('id'))
    if user:
        db.session.delete(user)
    # return jsonify({'success': True})
    return jsonify({'code': 200, 'msg': 'OK'})