# -*- coding: utf-8  -*-
# @Author: ty
# @File name: online.py 
# @IDE: PyCharm
# @Create time: 12/20/20 9:57 PM
from flask import render_template, request, jsonify

from app import base_blueprint
from app.models.OnLine import OnLine


@base_blueprint.route('/online/index', methods=['GET'])
def online_index():
    """

    :return:
    """
    return render_template('online/index.html')


@base_blueprint.route('/online/online_grid', methods=['POST'])
def online_grid():
    """

    :return:
    """
    page = request.form.get('page', 1, type=int)
    nums = request.form.get('nums', 10, type=int)
    pagination = OnLine.query.paginate(page=page, per_page=nums, error_out=False)

    onlines = pagination.items

    return jsonify({'total': OnLine.query.count(), 'nums': [online.to_json() for online in onlines]})