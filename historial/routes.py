from flask import render_template, request
from . import historial
from models import db, Pedidos, Clientes, DetallePedidos, Pizzas
from sqlalchemy import extract, func
from datetime import datetime

@historial.route("/", methods=["GET"])
def historial_pedidos():
    # Obtener parámetros del filtro
    tipo_filtro = request.args.get('tipo_filtro')
    dia_semana = request.args.get('dia_semana')
    mes = request.args.get('mes')
    
    pedidos = []
    
    if tipo_filtro == 'dia_semana' and dia_semana:
        try:
            dia_int = int(dia_semana)
            pedidos = Pedidos.query.join(Clientes).filter(
                func.weekday(Pedidos.fecha) == dia_int
            ).all()
        except ValueError:
            pedidos = []
            
    elif tipo_filtro == 'mes' and mes:
        try:
            mes_int = int(mes)
            pedidos = Pedidos.query.join(Clientes).filter(
                func.month(Pedidos.fecha) == mes_int
            ).all()
        except ValueError:
            pedidos = []
    else:
        # Sin filtro, mostrar todos
        pedidos = Pedidos.query.join(Clientes).all()
    
    return render_template(
        'historial/historial.html',
        pedidos=pedidos,
        tipo_filtro=tipo_filtro,
        dia_semana=dia_semana,
        mes=mes
    )

@historial.route("/detalle/<int:id>", methods=["GET"])
def detalle_pedido(id):
    # Obtener el pedido con su cliente
    pedido = Pedidos.query.get_or_404(id)
    
    # Obtener los detalles del pedido con las pizzas
    detalles = DetallePedidos.query.filter_by(id_pedido=id).join(Pizzas).all()
    
    return render_template(
        'historial/historial_detalle.html',
        pedido=pedido,
        detalles=detalles
    )