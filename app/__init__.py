from flask import Flask, render_template
from config import Config
from app.extensions import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models

    from app.clientes import bp_clientes
    from app.productos import bp_productos
    from app.pedidos import bp_pedidos

    app.register_blueprint(bp_clientes, url_prefix='/clientes')
    app.register_blueprint(bp_productos, url_prefix='/productos')
    app.register_blueprint(bp_pedidos, url_prefix='/pedidos')

    @app.route('/')
    def index():
        from app.models import Cliente, Producto, Pedido

        return render_template(
            'index.html',
            total_clientes=Cliente.query.count(),
            total_productos=Producto.query.count(),
            total_pedidos=Pedido.query.count()
        )

    return app