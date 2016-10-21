from flask import Blueprint

kebiao = Blueprint('kebiao', __name__)

from . import views
