from flask import Blueprint

bp_productos = Blueprint(
    'productos',
    __name__
)

from app.productos import routes