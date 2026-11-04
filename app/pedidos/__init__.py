from flask import Blueprint

bp_pedidos = Blueprint(
    'pedidos',
    __name__
)

from app.pedidos import routes