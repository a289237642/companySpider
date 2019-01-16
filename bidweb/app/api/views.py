#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from flask import request
from flask import jsonify, current_app
from flask_login import login_required
from elasticsearch.exceptions import NotFoundError

from app import elastic
from . import api
from .jsonfile import chinese, regions, websites


@api.route('/api/bids', methods=['GET'])
@login_required
def bids():
    index = current_app.config.get('ELASTICSEARCH_INDEX')
    doc_type = current_app.config.get('ELASTICSEARCH_TYPE')
    r = elastic.search(index=index, doc_type=doc_type)
    return jsonify(r)


@api.route('/bids', methods=['POST'])
@login_required
def get_bids():
    print(request.form)
    index = current_app.config.get('ELASTICSEARCH_INDEX')
    doc_type = current_app.config.get('ELASTICSEARCH_TYPE')

    end_dt = datetime.now()
    start_dt = end_dt - timedelta(days=7)
    end_string = end_dt.strftime('%Y-%m-%d')
    start_string = start_dt.strftime('%Y-%m-%d')

    # 需要验证起始时间小于截止时间
    sdate = request.form.get('sdate', start_string)
    edate = request.form.get('edate', end_string)
    sort = request.form.get('order[0][dir]', 'desc')

    region = request.form.get('region', '00')
    website = request.form.get('website', '000')
    word = request.form.get('word', '')

    start = request.form.get('start', default=0, type=int)
    length = request.form.get('length', default=12, type=int)

    body = dict(query={'bool': {'must': [], 'filter': []}})
    if word.strip():
        body['query']['bool']['must'].append({'match_phrase': {'details': word}})

    if region != '00':
        body['query']['bool']['filter'].append({'term': {'region': region}})

    if website != '000':
        body['query']['bool']['filter'].append({'term': {'site': website}})

    body['query']['bool']['filter'].append({'range': {'pubdate': {'gte': sdate, 'lte': edate}}})

    sort_s = "pubdate:{0}".format(sort)
    # result = elastic.search(index=index, doc_type=doc_type, body=body, size=length, _source_exclude=['details'],
    #                         from_=start, sort=[sort_string])
    result = elastic.search(index=index, doc_type=doc_type, body=body, size=length, _source_exclude=['details'],
                            from_=start, sort=[sort_s])
    ret = {'data': result['hits']['hits'], 'recordsTotal': result['hits']['total'], 'recordsFiltered': result['hits']['total']}

    # print(ret)
    return jsonify(ret)


@api.route('/bids/<id>', methods=['GET'])
@login_required
def get_bid(id):
    index = current_app.config.get('ELASTICSEARCH_INDEX')
    doc_type = current_app.config.get('ELASTICSEARCH_TYPE')
    try:
        result = elastic.get(index=index, doc_type=doc_type, id=id)
    except NotFoundError as e:
        # print(type(e.status_code))
        # print(type(e.info))
        # print(type(e.error))
        return jsonify(e.info)
    return jsonify(result)


@api.route('/json/chinese', methods=['GET'])
@login_required
def get_chinese():
    return jsonify(chinese)


@api.route('/json/regions', methods=['GET'])
@login_required
def get_regions():
    return jsonify(regions)


@api.route('/json/websites', methods=['GET'])
@login_required
def get_websites():
    return jsonify(websites)


