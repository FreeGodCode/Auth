# -*- coding: utf-8  -*-
# @Author: ty
# @File name: organization.py 
# @IDE: PyCharm
# @Create time: 12/20/20 6:20 PM
import uuid

from flask import render_template, request, jsonify
from flask_login import current_user

from app import base_blueprint, db
from app.models.Organization import Organization
from app.models.Resource import Resource
from app.models.User import User


@base_blueprint.route('/organization/index', methods=['GET'])
def organization_index():
    """

    :return:
    """
    return render_template('organization/index.html')


@base_blueprint.route('/organization/form', methods=['GET'])
def organization_form():
    """

    :return:
    """
    return render_template('organization/form.html', id=request.args.get('id', ''))


@base_blueprint.route('/organization/grant_resource', methods=['GET'])
def grant_organization_resource_page():
    """

    :return:
    """
    return render_template('organization/grant.html', id=request.args.get('id', ''))


@base_blueprint.route('/organization/grant', methods=['POST'])
def grant_organization_resource():
    """

    :return:
    """
    id = request.form.get('id', '')
    ids = request.form.get('ids', '')
    organization = Organization.query.get(id)
    if not ids:
        organization.resources = []
    else:
        id_list = ids.split(",")
        organization.resources = [Resource.query.get(r_id) for r_id in id_list]
    db.session.add(organization)
    # return jsonify({'success': True})
    return jsonify({'code': 200, 'msg': 'OK'})


@base_blueprint.route('/organization/tree_grid', methods=['POST'])
def organization_tree_grid():
    """

    :return:
    """
    organizations = Organization.query.all()
    return jsonify([organization.to_join() for organization in organizations])


# @base_blueprint.route('/organization/get_organization_comboxTree', methods=['POST'])
# def get_organization_comboxTree():
#     """
#
#     :return:
#     """
#     organizations = Organization.query.all()
#     return  jsonify([organization.to_join() for organization in organizations])


@base_blueprint.route('/organization/get_organizations_tree', methods=['POST'])
def get_organizations_tree():
    """

    :return:
    """
    organizations = Organization.query.join(User, Organization.users).filter(User.id == current_user.id).all()
    return jsonify([organization.to_join() for organization in organizations])


@base_blueprint.route('/organization/get_organization_by_id_notSecurity', methods=['POST'])
def get_organization_by_id():
    """

    :return:
    """
    organizations = Organization.query.join(User, Organization.users).filter(User.id == request.form.get('id')).all()
    return jsonify([organization.to_join() for organization in organizations])


@base_blueprint.route('/organization/get_organization_by_id', methods=['POST'])
def organization_by_id():
    """

    :return:
    """
    organization = Organization.query.get(request.form.get('id'))
    if organization:
        return jsonify(organization.to_join())
    else:
        # return jsonify({'success': False, 'msg': 'errors'})
        return jsonify({'code': 400, 'msg': 'errors'})


@base_blueprint.route('/organization/update', methods=['POST'])
def organization_update():
    """

    :return:
    """
    organization = Organization.query.get(request.form.get('data.id'))

    organization.name = request.form.get('data.name')
    organization.address = request.form.get('data.address')
    organization.code = request.form.get('data.code')
    organization.icons = request.form.get('data.icons')
    organization.seq = request.form.get('data.seq')
    organization.parent = request.form.get('data.parent')
    organization.update_time = request.form.get('data.update_time')

    db.session.add(organization)
    # return jsonify({"success": True})
    return jsonify({'code': 200, 'msg': 'OK'})


@base_blueprint.route('/organization/save', methods=['POST'])
def organization_save():
    """

    :return:
    """
    organization = Organization()
    organization.id = str(uuid.uuid4())
    organization.name = request.form.get('data.name')
    organization.address = request.form.get('data.address')
    organization.code = request.form.get('data.code')
    organization.icons = request.form.get('data.icons')
    organization.seq = request.form.get('data.seq')
    organization.parent = Organization.query.get(request.form.get('data.organization.id'))
    current_user.organizations.append(organization)

    db.session.add(organization)
    # return jsonify({'success': True})
    return jsonify({'code': 200, 'msg': 'OK'})


@base_blueprint.route('/organization/delete', methods=['POST'])
def organization_delete():
    """

    :return:
    """
    organization = Organization.query.get(request.form.get('id'))
    if organization:
        db.session.delete(organization)

    # return jsonify({'success': True})
    return jsonify({'code': 200, 'msg': 'OK'})