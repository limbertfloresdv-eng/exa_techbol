from datetime import datetime

from flask import render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import Pedido, Cliente, Producto
from app.pedidos import bp_pedidos


@bp_pedidos.route('/')
def index():
    pedidos = Pedido.query.order_by(Pedido.id.desc()).all()

    return render_template(
        'pedidos/index.html',
        pedidos=pedidos
    )


@bp_pedidos.route('/crear', methods=['GET', 'POST'])
def crear():
    clientes = Cliente.query.all()
    productos = Producto.query.all()

    if request.method == 'POST':
        try:
            cliente_id = int(request.form['cliente_id'])
            producto_id = int(request.form['producto_id'])
            monto = float(request.form['monto'])
            fecha = datetime.strptime(
                request.form['fecha'], '%Y-%m-%d'
            ).date()

            cliente = db.session.get(Cliente, cliente_id)
            producto = db.session.get(Producto, producto_id)

            if not cliente or not producto or monto < 0:
                raise ValueError

            pedido = Pedido(
                cliente_id=cliente_id,
                producto_id=producto_id,
                monto=monto,
                fecha=fecha
            )

            db.session.add(pedido)
            db.session.commit()

            flash('Pedido registrado correctamente.', 'success')
            return redirect(url_for('pedidos.index'))

        except (ValueError, TypeError):
            flash('Verifica los datos del pedido.', 'danger')

    return render_template(
        'pedidos/form.html',
        pedido=None,
        clientes=clientes,
        productos=productos
    )


@bp_pedidos.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pedido = db.get_or_404(Pedido, id)
    clientes = Cliente.query.all()
    productos = Producto.query.all()

    if request.method == 'POST':
        try:
            cliente_id = int(request.form['cliente_id'])
            producto_id = int(request.form['producto_id'])
            monto = float(request.form['monto'])
            fecha = datetime.strptime(
                request.form['fecha'], '%Y-%m-%d'
            ).date()

            if not db.session.get(Cliente, cliente_id):
                raise ValueError

            if not db.session.get(Producto, producto_id) or monto < 0:
                raise ValueError

            pedido.cliente_id = cliente_id
            pedido.producto_id = producto_id
            pedido.monto = monto
            pedido.fecha = fecha

            db.session.commit()

            flash('Pedido actualizado correctamente.', 'success')
            return redirect(url_for('pedidos.index'))

        except (ValueError, TypeError):
            flash('Verifica los datos del pedido.', 'danger')

    return render_template(
        'pedidos/form.html',
        pedido=pedido,
        clientes=clientes,
        productos=productos
    )


@bp_pedidos.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    pedido = db.get_or_404(Pedido, id)

    db.session.delete(pedido)
    db.session.commit()

    flash('Pedido eliminado correctamente.', 'success')
    return redirect(url_for('pedidos.index'))