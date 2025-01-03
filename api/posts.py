from datetime import datetime
from flask import Blueprint, jsonify, request, make_response
from . import db
from api.models import *
from api.error_handler import APIException

bp = Blueprint('blogging', __name__)


def make_response(data=None, message='operation completed successfully', status='success', status_code=200):
    response = {
        'status': status,
        'message': message,
        'data': data
    }
    return jsonify(response), status_code


@bp.errorhandler(APIException)
def handle_api_error(e):
    response = e.to_dict()
    return jsonify(response), e.status_code


def process_tags(article, tags):
    if not tags:
        raise APIException(message='tags cannot be empty')

    tag_list = []
    if isinstance(tags, list):
        for tag_name in tags:
            tag = Tags.query.filter_by(tags=tag_name).first()
            if not tag:
                tag = Tags(tags=tag_name)
                tag_list.append(tag)
            else:
                tag_list.append(tag)
        db.session.add_all(tag_list)
    else:
        raise APIException(message='invalid tags format')
    article.tagging.extend(tag_list)


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
            tags = data['tags']
        except ValueError as e:
            db.session.rollback()
            raise APIException(message=str(e), status_code=400)
        except KeyError as e:
            db.session.rollback()
            raise APIException(
                message=f'missing required key: {e}', status_code=400)
        db.session.add(article)
        process_tags(article, tags)
        db.session.commit()
        return make_response(status_code=201)
    raise APIException(message='invalid JSON')


@bp.route('/posts/<int:id>', methods=['PUT'])
def update(id):
    article = Article.query.filter_by(_id=id).first()
    if article:
        if request.is_json:
            try:
                data = request.get_json()
                article.title = data['title']
                article.content = data['content']
                article.category = data['category']
                article.updatedAt = datetime.strptime(datetime.now().strftime(
                    "%Y-%m-%dT%H:%M:%S"), "%Y-%m-%dT%H:%M:%S")
                tags = data['tags']
            except ValueError as e:
                db.session.rollback()
                raise APIException(message=str(e), status_code=400)
            except KeyError as e:
                db.session.rollback()
                raise APIException(
                    message=f'missing required key: {e}', status_code=400)
            process_tags(article, tags)
            db.session.commit()
            return make_response(status_code=200)
        raise APIException(message='invalid JSON')
    raise APIException(message='post not found')


@bp.route('/posts', methods=['GET'])
@bp.route('/posts/<int:id>', methods=['GET'])
def get(id=None):
    if id:
        article = Article.query.filter_by(_id=id).first()
        if not article:
            raise APIException(message='post not found')
        data = article.to_dict()
        return make_response(data=data)

    articles = Article.query.all()
    data = [article.to_dict() for article in articles]
    return make_response(data=data)


@bp.route('/posts/<int:id>', methods=['DELETE'])
def delete(id=None):
    article = Article.query.filter_by(_id=id).first()
    if article:
        db.session.delete(article)
        db.session.commit()
        return make_response(status_code=204)
    raise APIException(message='post not found')
