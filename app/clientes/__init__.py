from flask import Blueprint

bp_clientes = Blueprint(
    'clientes',
    __name__
)

from app.clientes import routes