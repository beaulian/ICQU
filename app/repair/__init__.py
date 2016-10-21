from flask import Blueprint

repair = Blueprint('repair', __name__)

from . import views