from flask import render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import Cliente
from app.clientes import bp_clientes


@bp_clientes.route('/')
def index():
    clientes = Cliente.query.order_by(Cliente.id.desc()).all()
    return render_template('clientes/index.html', clientes=clientes)


@bp_clientes.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        telefono = request.form['telefono'].strip()

        if not nombre or not telefono:
            flash('Completa todos los campos.', 'warning')
            return redirect(url_for('clientes.crear'))

        cliente = Cliente(nombre=nombre, telefono=telefono)
        db.session.add(cliente)
        db.session.commit()

        flash('Cliente registrado correctamente.', 'success')
        return redirect(url_for('clientes.index'))

    return render_template('clientes/form.html', cliente=None)


@bp_clientes.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cliente = db.get_or_404(Cliente, id)

    if request.method == 'POST':
        cliente.nombre = request.form['nombre'].strip()
        cliente.telefono = request.form['telefono'].strip()

        if not cliente.nombre or not cliente.telefono:
            flash('Completa todos los campos.', 'warning')
            return redirect(url_for('clientes.editar', id=id))

        db.session.commit()
        flash('Cliente actualizado correctamente.', 'success')
        return redirect(url_for('clientes.index'))

    return render_template('clientes/form.html', cliente=cliente)


@bp_clientes.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    cliente = db.get_or_404(Cliente, id)

    db.session.delete(cliente)
    db.session.commit()

    flash('Cliente eliminado correctamente.', 'success')
    return redirect(url_for('clientes.index'))