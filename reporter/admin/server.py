import logging


from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from .admin_api import admin_api_blueprint


logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__, static_folder="frontend_dist", static_url_path="/static")

    # Add prometheus wsgi middleware to route /metrics requests
    prometheus_wsgi_app = make_wsgi_app()
    app.wsgi_app = DispatcherMiddleware(
        app.wsgi_app,
        {
            "/metrics": prometheus_wsgi_app,
        },
    )
    app.register_blueprint(admin_api_blueprint)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        return app.send_static_file("index.html")

    return app
