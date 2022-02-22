import os


def get_env_variable(var_name, default=None):
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        raise RuntimeError(
            "The environment variable {} was missing, abort...".format(var_name)
        )


ROW_LIMIT = 5000

SUPERSET_WEBSERVER_PORT = 8088

SECRET_KEY = get_env_variable("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = get_env_variable("DATABASE_URL")

MAPBOX_API_KEY = get_env_variable("MAPBOX_API_KEY")
