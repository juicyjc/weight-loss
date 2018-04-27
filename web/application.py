from flask import Flask

def create_app(**config_overrides):
    app = Flask(__name__)

    # Load config
    app.config.from_pyfile('settings.py')

    # apply overrides for tests
    app.config.update(config_overrides)

    # import blueprints
    from home.views import home_app
    # from entry.views import entry_app
    # from app.views import app_app

    # register blueprints
    app.register_blueprint(home_app)
    # app.register_blueprint(entry_app)
    # app.register_blueprint(app_app)

    return app
