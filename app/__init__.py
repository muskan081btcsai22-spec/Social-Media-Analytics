import os
from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient

login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
    db_name = os.environ.get('MONGO_DBNAME', 'sma_db')
    client = MongoClient(mongo_uri)
    app.db = client[db_name]
    # feedparser does not require a token by default; keep other config via env vars

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # register blueprints (moved to project-root `routes` package)
    from routes.auth import auth_bp
    from routes.cases import cases_bp
    from routes.trending import trending_bp
    from routes.fakenews import fakenews_bp
    from routes.ad_campaign import ad_bp
    from routes.realtime import realtime_bp
    from routes.competitor import competitor_bp
    app.register_blueprint(auth_bp, url_prefix='')
    app.register_blueprint(cases_bp, url_prefix='')
    app.register_blueprint(trending_bp, url_prefix='')
    app.register_blueprint(fakenews_bp, url_prefix='')
    app.register_blueprint(ad_bp, url_prefix='')
    app.register_blueprint(realtime_bp, url_prefix='')
    app.register_blueprint(competitor_bp, url_prefix='')

    @login_manager.user_loader
    def load_user(user_id):
        from .models.user import User
        return User.get_by_id(app.db, user_id)

    return app
