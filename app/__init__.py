from flask import Flask
from app.routes.main import main_bp
from app.routes.api import api_bp


def create_app():
    app = Flask(__name__)

    # ルートの登録
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    return app
