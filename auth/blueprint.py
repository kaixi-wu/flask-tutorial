from flask import Blueprint

auth_blue = Blueprint('auth', __name__)

import auth.views.auth