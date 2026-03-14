from flask import render_template, request, redirect, url_for, session, flash
from calendar import monthrange
from . import pedidos
import forms
from models import db, Clientes, Pedidos, Pizzas, DetallePedidos
from datetime import datetime

PRECIOS_TAMANO = {'Chica': 40, 'Mediana': 80, 'Grande': 120}
PRECIO_INGREDIENTE = 10

@pedidos.route("/", methods=["GET", "POST"])
def index():
    form = forms.PedidoForm(request.form)
    
    if 'carrito' not in session:
        session['carrito'] = []

    if request.method == 'POST' and 'agregar' in request.form:
        tamano = request.form.get('tamano')
        ingredientes_lista = request.form.getlist('ingredientes')
        num_pizzas = int(request.form.get('num_pizzas', 1))
        
        if len(session['carrito']) > 0:
            if not all(k in session for k in ['dia_pedido', 'mes_pedido', 'anio_pedido']):
                flash("Error: No hay fecha de pedido guardada")
                return redirect(url_for('pedidos.index'))
        else:
            dia = request.form.get('dia')
            mes = request.form.get('mes')
            anio = request.form.get('anio')
            
            if not dia or not mes or not anio:
                flash("Debes seleccionar una fecha completa para el pedido")
                return redirect(url_for('pedidos.index'))
            
            # ===== VALIDACIÓN DE FECHA =====
            try:
                dia_int = int(dia)
                mes_int = int(mes)
                anio_int = int(anio)
                
                # Validar mes
                if mes_int < 1 or mes_int > 12:
                    flash("Mes inválido (debe ser 1-12)")
                    return redirect(url_for('pedidos.index'))
                
                # Validar días por mes
                dias_en_mes = monthrange(anio_int, mes_int)[1]
                if dia_int < 1 or dia_int > dias_en_mes:
                    flash(f"Día inválido para el mes seleccionado. {mes_int}/{anio_int} tiene {dias_en_mes} días")
                    return redirect(url_for('pedidos.index'))
                
                # Validar año
                if anio_int < 2000 or anio_int > 2100:
                    flash("Año inválido (debe ser entre 2000 y 2100)")
                    return redirect(url_for('pedidos.index'))
                    
            except ValueError:
                flash("Formato de fecha inválido")
                return redirect(url_for('pedidos.index'))
            
            # Guardar la fecha en sesión
            session['dia_pedido'] = dia
            session['mes_pedido'] = mes
            session['anio_pedido'] = anio
            session['nombre_cliente'] = request.form.get('nombre_cliente')
            session['direccion'] = request.form.get('direccion')
            session['telefono'] = request.form.get('telefono')
        
        # Calcular precios
        precio_unidad = PRECIOS_TAMANO.get(tamano, 0) + (len(ingredientes_lista) * PRECIO_INGREDIENTE)
        subtotal = precio_unidad * num_pizzas

        item = {
            'tamano': tamano,
            'ingredientes': ", ".join(ingredientes_lista),
            'num_pizzas': num_pizzas,
            'subtotal': subtotal
        }
        session['carrito'].append(item)
        session.modified = True
        
        flash(f"Pizza agregada al carrito. Fecha del pedido: {session['dia_pedido']}/{session['mes_pedido']}/{session['anio_pedido']}")
        return redirect(url_for('pedidos.index'))

    datos_cliente = {
        'nombre_cliente': session.get('nombre_cliente', ''),
        'direccion': session.get('direccion', ''),
        'telefono': session.get('telefono', ''),
        'dia': session.get('dia_pedido', ''),
        'mes': session.get('mes_pedido', ''),
        'anio': session.get('anio_pedido', '')
    }
    
    total_venta = sum(item['subtotal'] for item in session['carrito'])
    return render_template("pedidos/index.html", 
                         form=form, 
                         detalle=session['carrito'], 
                         total=total_venta,
                         datos=datos_cliente)

@pedidos.route("/quitar/<int:id>", methods=["POST"])
def quitar(id):
    if 'carrito' in session and 0 <= id < len(session['carrito']):
        session['carrito'].pop(id)
        session.modified = True
        
        if len(session['carrito']) == 0:
            session.pop('dia_pedido', None)
            session.pop('mes_pedido', None)
            session.pop('anio_pedido', None)
            session.pop('nombre_cliente', None)
            session.pop('direccion', None)
            session.pop('telefono', None)
            
    return redirect(url_for('pedidos.index'))

@pedidos.route("/cancelar_pedido", methods=["POST"])
def cancelar_pedido():
    """Cancela todo el pedido actual"""
    session.pop('carrito', None)
    session.pop('nombre_cliente', None)
    session.pop('direccion', None)
    session.pop('telefono', None)
    session.pop('dia_pedido', None)
    session.pop('mes_pedido', None)
    session.pop('anio_pedido', None)
    flash("Pedido cancelado")
    return redirect(url_for('pedidos.index'))

@pedidos.route("/terminar", methods=["POST"])
def terminar():
    carrito = session.get('carrito', [])
    if not carrito:
        flash("El carrito está vacío")
        return redirect(url_for('pedidos.index'))

    if not all(k in session for k in ['nombre_cliente', 'direccion', 'telefono', 'dia_pedido', 'mes_pedido', 'anio_pedido']):
        flash("Error: Datos del pedido incompletos")
        return redirect(url_for('pedidos.index'))

    # Crear Cliente
    nuevo_cliente = Clientes(
        nombre=session.get('nombre_cliente'),
        direccion=session.get('direccion'),
        telefono=session.get('telefono')
    )
    db.session.add(nuevo_cliente)
    db.session.flush()

    # Crear Pedido con la fecha
    fecha_str = f"{session.get('anio_pedido')}-{session.get('mes_pedido')}-{session.get('dia_pedido')}"
    try:
        fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d')
    except ValueError:
        flash("Error en el formato de la fecha")
        return redirect(url_for('pedidos.index'))
        
    total_venta = sum(item['subtotal'] for item in carrito)
    
    nuevo_pedido = Pedidos(id_cliente=nuevo_cliente.id_cliente, fecha=fecha_dt, total=total_venta)
    db.session.add(nuevo_pedido)
    db.session.flush()

    # Crear Detalles del pedido
    for item in carrito:
        nueva_pizza = Pizzas(
            tamano=item['tamano'], 
            ingredientes=item['ingredientes'], 
            precio=item['subtotal'] / item['num_pizzas']
        )
        db.session.add(nueva_pizza)
        db.session.flush()
        
        detalle = DetallePedidos(
            id_pedido=nuevo_pedido.id_pedido, 
            id_pizza=nueva_pizza.id_pizza, 
            cantidad=item['num_pizzas'], 
            subtotal=item['subtotal']
        )
        db.session.add(detalle)

    db.session.commit()
    
    # Limpiar todo de la sesión
    session.pop('carrito', None)
    session.pop('nombre_cliente', None)
    session.pop('direccion', None)
    session.pop('telefono', None)
    session.pop('dia_pedido', None)
    session.pop('mes_pedido', None)
    session.pop('anio_pedido', None)
    
    flash(f"Pedido registrado con éxito para la fecha {fecha_str}")
    return redirect(url_for('pedidos.index'))