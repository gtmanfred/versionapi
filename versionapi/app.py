# -*- coding: utf-8 -*-

# Import Python Libraries
import importlib.util
import inspect
import os

# Import Flask Libraries
import flask
import flask_restful

load_objects = [
    flask,
    flask_restful,
]


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for obj in load_objects:
        if isinstance(obj, tuple):
            setattr(module, f'__{obj[0]}__', obj[1])
        else:
            setattr(module, f'__{obj.__name__}__', obj)
    return module


def create_resource(blueprint):
    setattr(
        blueprint,
        'methods',
        list(map(
            lambda item: next(iter(item)).upper(),
            inspect.getmembers(blueprint, inspect.isfunction)
        ))
    )
    return type(blueprint.__name__, (blueprint, flask_restful.Resource), {})


def create_blueprint_app(modapp):
    version = getattr(modapp, '__version__', 1)
    app = flask.Blueprint(modapp.__name__, modapp.__name__)
    api = flask_restful.Api(app)
    for obj in inspect.getmembers(modapp, inspect.isclass):
        blueprint = obj[1]
        if hasattr(blueprint, 'uri'):
            api.add_resource(create_resource(blueprint), f'/api/v{version}{blueprint.uri}')
    return app


def setup_app():
    app = flask.Flask(__name__)
    app.config['DEBUG'] = bool(os.environ.get('FLASK_DEBUG', False))

    if app.config['DEBUG'] is True:
        @app.route('/html/<path:path>')
        def send_html(path):
            return flask.send_from_directory('html', path)

    @app.after_request
    def apply_caching(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS, HEAD, PUT, DELETE'
        return response

    global load_objects
    load_objects.extend([])

    with os.scandir(os.path.dirname(__file__)) as rit:
        for entry in rit:
            if entry.name[0] not in ('.', '_') and entry.is_dir():
                modfile = f'{entry.path}/app.py'
                if not os.path.isfile(modfile):
                    continue
                modname = f'versionapi.{os.path.basename(entry.path)}.app'
                app.register_blueprint(create_blueprint_app(_load_module(modname, modfile)))
    return app


if __name__ == '__main__':
    setup_app().run(host='0.0.0.0', port=5000)
