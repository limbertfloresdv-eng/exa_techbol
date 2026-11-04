from flask import render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import Producto
from app.productos import bp_productos


@bp_productos.route('/')
def index():
    productos = Producto.query.order_by(Producto.id.desc()).all()
    return render_template('productos/index.html', productos=productos)


@bp_productos.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre'].strip()
            precio = float(request.form['precio'])
            stock = int(request.form['stock'])

            if not nombre or precio < 0 or stock < 0:
                raise ValueError

            producto = Producto(
                nombre=nombre,
                precio=precio,
                stock=stock
            )

            db.session.add(producto)
            db.session.commit()

            flash('Producto registrado correctamente.', 'success')
            return redirect(url_for('productos.index'))

        except ValueError:
            flash('Verifica el nombre, precio y stock.', 'danger')

    return render_template('productos/form.html', producto=None)


@bp_productos.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    producto = db.get_or_404(Producto, id)

    if request.method == 'POST':
        try:
            nombre = request.form['nombre'].strip()
            precio = float(request.form['precio'])
            stock = int(request.form['stock'])

            if not nombre or precio < 0 or stock < 0:
                raise ValueError

            producto.nombre = nombre
            producto.precio = precio
            producto.stock = stock

            db.session.commit()

            flash('Producto actualizado correctamente.', 'success')
            return redirect(url_for('productos.index'))

        except ValueError:
            flash('Verifica los datos ingresados.', 'danger')

    return render_template('productos/form.html', producto=producto)


@bp_productos.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    producto = db.get_or_404(Producto, id)

    db.session.delete(producto)
    db.session.commit()

    flash('Producto eliminado correctamente.', 'success')
    return redirect(url_for('productos.index'))