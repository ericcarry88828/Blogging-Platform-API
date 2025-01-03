from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    app.json.sort_keys = False

    db.init_app(app)

    with app.app_context():
        from . import models

    from . import posts
    app.register_blueprint(posts.bp)

    @app.errorhandler(405)
    def method_not_allow(e):
        return jsonify({'status': 'error', 'message': 'please use correct method to access this endpoint.', 'error': 'method not allowed'})

    return app
