from flask import Blueprint

historial = Blueprint(
    'historial', 
    __name__,
    template_folder='templates',
    static_folder='static'
)

from . import routes