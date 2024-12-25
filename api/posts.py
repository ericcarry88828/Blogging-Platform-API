from datetime import datetime
from urllib import response
from flask import Blueprint, json, jsonify, request, Response
from werkzeug.exceptions import *
from . import db
from api.models import *

bp = Blueprint('blogging', __name__)


@bp.errorhandler(ValueError)
def handle_value_error(error):
    response = jsonify({'error': 'operation failed', 'msg': str(error)})
    response.status_code = 400
    return response


@bp.errorhandler(KeyError)
def handle_key_error(error):
    response = jsonify({'error': 'operation failed',
                       'msg': 'Missing required keys: ' + str(error)})
    response.status_code = 400
    return response


def make_error_response(status_code, msg, error='Operation Failed') -> HTTPException:
    response = jsonify({'error': error, 'msg': msg})
    if status_code == 400:
        return BadRequest(response=response)
    elif status_code == 404:
        return NotFound(response=response)


@bp.route('/posts', methods=['POST'])
def create():
    if request.is_json:
        data = request.get_json()
        try:
            now = datetime.strptime(datetime.now().strftime(
                "%Y-%m-%dT%H:%M:%S"), "%Y-%m-%dT%H:%M:%S")
            article = Article(title=data['title'],
                              content=data['content'],
                              category=data['category'],
                              createdAt=now,
                              updatedAt=now
                              )
        except ValueError as e:
            db.session.rollback()
            return handle_value_error(e)
        except KeyError as e:
            db.session.rollback()
            return handle_key_error(e)
        db.session.add(article)

        tags = data['tags']
        if not tags:
            db.session.rollback()
            raise ValueError('tags is required')
        for tag_name in tags:
            tag = Tags.query.filter_by(tags=tag_name).first()
            if not tag:
                tag = Tags(tags=tag_name)
                db.session.add(tag)
            article.tagging.append(tag)
        db.session.commit()
        return jsonify({'msg': 'Operation Successed'}), 201
    raise make_error_response(400, 'Invalid JSON')


@bp.route('/posts/<int:id>', methods=['PUT'])
def update(id):
    article = Article.query.filter_by(_id=id).first()
    if article:
        try:
            data = request.get_json()
            article.title = data['title']
            article.content = data['content']
            article.category = data['category']
            article.updatedAt = datetime.strptime(datetime.now().strftime(
                "%Y-%m-%dT%H:%M:%S"), "%Y-%m-%dT%H:%M:%S")
        except ValueError as e:
            db.session.rollback()
            return handle_value_error(e)
        except KeyError as e:
            db.session.rollback()
            return handle_key_error(e)

        tags = data['tags']
        if not tags:
            db.session.rollback()
            raise ValueError('tags is required')

        article.tagging.clear()
        for tag_name in tags:
            tag = Tags.query.filter_by(tags=tag_name).first()
            if not tag:
                tag = Tags(tags=tag_name)
                db.session.add(tag)
            if tag not in article.tagging:
                article.tagging.append(tag)
        db.session.commit()
        return jsonify({'msg': 'Operation Successed'}), 200
    raise make_error_response(404, 'Post Not Found')


@bp.route('/posts', methods=['GET'])
@bp.route('/posts/<int:id>', methods=['GET'])
def get(id=None):
    if id:
        article = Article.query.filter_by(_id=id).first()
        if not article:
            raise make_error_response(404, 'Post Not Found')
        response = json.dumps(
            article.to_dict(), sort_keys=False)
        return Response(response, mimetype='application/json')

    articles = Article.query.all()
    response = json.dumps([article.to_dict()
                          for article in articles], sort_keys=False)
    return Response(response, mimetype='application/json')


@bp.route('/posts/<int:id>', methods=['DELETE'])
def delete(id=None):
    article = Article.query.filter_by(_id=id).first()
    if article:
        db.session.delete(article)
        db.session.commit()
        return ('', 204)
    return make_error_response(404, 'Post Not Found')
