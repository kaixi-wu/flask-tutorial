from flask import Blueprint

business_blue = Blueprint('business', __name__)

import business.views.business
