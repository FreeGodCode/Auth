# -*- coding: utf-8  -*-
# @Author: ty
# @File name: resource.py 
# @IDE: PyCharm
# @Create time: 12/20/20 5:13 PM
import uuid

from flask import jsonify, render_template, request
from flask_login import current_user

from app import base_blueprint, db
from app.models.Organization import Organization
from app.models.Resource import Resource
from app.models.ResourceType import ResourceType
from app.models.Role import Role
from app.models.User import User


@base_blueprint.route('/resource/get_main_menu', methods=['POST'])
def get_resource_grid():
    """

    :return:
    """
    # resource = db.session.query(Resource).join(Role, Resource.roles).
    resources = Resource.query.join(Role, Resource.roles).join(User, Role.users).filter(
        User.id == current_user.id).all()
    return jsonify([resource.to_menu_json() for resource in resources])


@base_blueprint.route('/resource/type_combox', methods=['POST'])
def resource_type_combox():
    """

    :return:
    """
    resource_types = ResourceType.query.all()
    return jsonify([resource_type.to_join() for resource_type in resource_types])


@base_blueprint.route('/resource/index', methods=['GET'])
def resource_index():
    """

    :return:
    """
    return render_template('resource/index.html')


@base_blueprint.route('/resource/form', methods=['GET'])
def resource_form():
    """

    :return:
    """
    return render_template('resource/form.html', id=request.args.get('id', ''))


@base_blueprint.route('/resource/get_role_resources', methods=['POST'])
def get_role_resources():
    """

    :return:
    """
    resources = Resource.query.join(Role, Resource.roles).filter(Role.id == request.form.get('id')).all()
    return jsonify([resource.to_join() for resource in resources])


@base_blueprint.route('/resource_treeGrid', methods=['POST'])
def resource_treeGrid():
    """

    :return:
    """
    resource_list = Resource.query.all()
    return jsonify([resource.to_join() for resource in resource_list])


@base_blueprint.route('/resource/get_resource_tree', methods=['POST'])
def get_resources_tree():
    """

    :return:
    """
    return resource_treeGrid()


@base_blueprint.route('/resource/get_organization_resources', methods=['POST'])
def get_organization_resources():
    """

    :return:
    """
    resources = Resource.query.join(Organization, Resource.organization).filter(
        Organization.id == request.form.get('id')).all()
    return jsonify([resource.to_join() for resource in resources])


@base_blueprint.route('/resource/getById', methods=['POST'])
def resource_get_by_id():
    """

    :return:
    """
    resource = Resource.query.get(request.form.get('id'))
    if resource:
        return jsonify(resource.to_join())
    else:
        # return jsonify({'success': False, 'msg': 'error})
        return jsonify({'code': 400, 'msg': 'error'})


@base_blueprint.route('/resource/update', methods=['POST'])
def resource_update():
    """

    :return:
    """
    resource = Resource.query.get(request.form.get('data.id'))
    resource.name = request.form.get('data.name')
    resource.url = request.form.get('data.url')
    resource.desc = request.form.get('data.desc')
    resource.icons = request.form.get('data.icons')
    resource.seq = request.form.get('data.seq')
    resource.target = request.form.get('data.target')
    resource.update_time = request.form.get('data.update_time')
    resource.resource_id = request.form.get('data.resource_id')
    resource.parent = request.form.get('data.parent')

    db.session.add(resource)
    # return jsonify({"success": True})
    return jsonify({'code': 200, 'msg': 'OK'})


@base_blueprint.route('/resource/save', methods=['POST'])
def resource_save():
    """

    :return:
    """
    resource = Resource()
    resource.id = str(uuid.uuid4())
    resource.name = request.form.get('data.name')
    resource.url = request.form.get('data.url')
    resource.desc = request.form.get('data.desc')
    resource.icons = request.form.get('data.icons')
    resource.seq = request.form.get('data.seq')
    resource.target = request.form.get('data.target')
    resource.resource_id = request.form.get('data.resource_id')
    resource.parent = request.form.get('data.parent')
    resource.update_time = request.form.get('data.update_time')
    db.session.add(resource)
    # return jsonify({'success': True})
    return jsonify({'code': 200, 'msg': 'OK'})


@base_blueprint.route('/resource/delete', methods=['POST'])
def resource_delete():
    """

    :return:
    """
    resource = Resource.query.get(request.form.get('id'))
    if resource:
        db.session.delete(resource)

    # return jsonify({'success': True})
    return jsonify({'code': 200, 'msg': 'OK'})