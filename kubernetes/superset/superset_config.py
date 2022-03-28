import os

from flask_appbuilder.security.manager import AUTH_OAUTH
from superset.security import SupersetSecurityManager


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

NEATPLUS_URL = get_env_variable("NEATPLUS_URL")

AUTH_TYPE = AUTH_OAUTH
OAUTH_PROVIDERS = [
    {
        "name": "neatplus",
        "token_key": "access_token",
        "icon": "fa-address-card",
        "remote_app": {
            "client_id": get_env_variable("OAUTH_CLIENT_ID"),
            "client_secret": get_env_variable("OAUTH_CLIENT_SECRET"),
            "client_kwargs": {"scope": "read"},
            "access_token_method": "POST",
            "api_base_url": f"{NEATPLUS_URL}/api/v1/",
            "access_token_url": f"{NEATPLUS_URL}/oauth/token/",
            "authorize_url": f"{NEATPLUS_URL}/oauth/authorize/",
        },
    }
]

AUTH_USER_REGISTRATION = True

AUTH_ROLES_MAPPING = {"superuser": ["Admin"], "non_superuser": ["Gamma"]}


class CustomSsoSecurityManager(SupersetSecurityManager):
    def oauth_user_info(self, provider, response=None):
        if provider == "neatplus":
            me = self.appbuilder.sm.oauth_remotes[provider].get("user/me").json()
            user_role = me.get["isSuperuser"]
            if user_role:
                role_keys = ["superuser"]
            else:
                role_keys = ["non_superuser"]
            return {
                "email": me["email"],
                "username": me["username"],
                "first_name": me["firstName"],
                "last_name": me["lastName"],
                "role_keys": role_keys,
            }


CUSTOM_SECURITY_MANAGER = CustomSsoSecurityManager
