# -*- coding: utf-8  -*-
# @Author: ty
# @File name: user.py 
# @IDE: PyCharm
# @Create time: 12/19/20 4:56 PM
import uuid
from datetime import datetime

from flask import render_template, request, jsonify
from flask_login import current_user

from app import base_blueprint, db
from app.models.Resource import Resource
from app.models.Role import Role
from app.models.User import User


@base_blueprint.route('/role', methods=['GET'])
def role_index():
    """

    :return:
    """
    return render_template('role/index.html')


@base_blueprint.route('/role_form ', methods=['GET'])
def role_form():
    """

    :return:
    """
    return render_template('role/form.html', id=request.args.get('id', ''))



@base_blueprint.route('/grant_role_page', methods=['GET'])
def grant_role_page():
    """

    :return:
    """
    return render_template('role/grant_role.html', id=request.form.get('id', ''))


@base_blueprint.route('/get_roles_tree', methods=['POST'])
def get_roles_tree():
    """

    :return:
    """
    roles = db.session.query.get(User).join(User, Role.users).filter(User.id == current_user.id).all()
    # roles = Role.query.join(User, Role.users).filter(User.id == current_user.id).all()
    return jsonify([role.to_join() for role in roles])


@base_blueprint.route('/get_role_by_userId', methods=['POST'])
def get_roles_by_userId():
    """

    :return:
    """
    roles = Role.query.join(User, Role.users).filter(User.id == request.form.get('id')).all()
    # roles = db.session.query(Role).join(User, Role.users).filter(User.id == request.form.get('id')).all()
    return jsonify([role.to_join() for role in roles])


@base_blueprint.route('/grant_role', methods=['POST'])
def grant_role():
    """

    :return:
    """
    id = request.form.get('id', '')
    ids = request.form.get('ids', '')

    role = db.session.query(Role).get(id)

    # 授权资源为空
    if not ids:
        role.resources = []
    # 授权资源访问,资源之间用逗号分隔
    else:
        id_list = ids.split(',')
        role.resources = [db.session.query(Resource).get(r_id) for r_id in id_list]

    db.session.add(role)
    return jsonify({'success': True})


@base_blueprint.route('/role_grid', methods=['POST'])
def role_grid():
    """
    角色分页显示
    :return:
    """
    page = request.form.get('page', 1, type=int)
    nums = request.form.get('nums', 10, type=int)

    # def paginate(self, page=None, per_page=None, error_out=True, max_per_page=None):
    pagination = current_user.roles.paginate(page=page, per_page=nums, error_out=False)
    roles = pagination.items
    return jsonify([role.to_join() for role in roles])


@base_blueprint.route('/role_update', methods=['POST'])
def role_update():
    """
    更新角色
    :return:
    """
    role = db.session.query(Role).get(request.form.get('data.id'))
    if not role:
        return jsonify({'success': False, 'msg': '参数有误'})

    role.name = request.form.get('data.name')
    role.desc = request.form.get('data.desc')
    role.seq = request.form.get('data.seq')
    role.update_time = datetime.now()
    db.session.add(role)
    return jsonify({'success': True})


@base_blueprint.route('/role_save', methods=['POST'])
def role_save():
    """
    新建角色
    :return:
    """
    role = Role()
    role.id = str(uuid.uuid4())
    role.name = request.form.get('data.name')
    role.desc = request.form.get('data.desc')
    role.seq = request.form.get('data.seq')
    current_user.roles.append(role)
    db.session.add(role)
    return jsonify({'success': True})


@base_blueprint.route('role_delete', methods=['POST'])
def role_delete():
    """
    删除角色
    :return:
    """
    role = db.session.query(Role).get(request.form.get('id', ''))
    if role:
        db.session.delete(role)
    return jsonify({'success': True})
