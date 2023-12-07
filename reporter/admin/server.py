import os
import logging
from pathlib import Path


from flask import Flask, jsonify, render_template, request
from reporter.version import VERSION
from prometheus_client import Gauge, Counter, Histogram, Info
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app


logger = logging.getLogger(__name__)


def create_app(prefix):
    app = Flask(__name__)

    # Add prometheus wsgi middleware to route /metrics requests
    prometheus_wsgi_app = make_wsgi_app()
    app.wsgi_app = DispatcherMiddleware(
        app.wsgi_app,
        {
            "/metrics": prometheus_wsgi_app,
            f"{prefix}/metrics": prometheus_wsgi_app,
        },
    )

    @app.route(f"{prefix}/")
    def home():
        return "hello, admin"

    return app
