from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

import datetime

db=SQLAlchemy()
class Pizzas(db.Model):
    __tablename__='pizzas'
    id_pizza=db.Column(db.Integer, primary_key=True)
    tamano=db.Column(db.String(20))
    ingredientes=db.Column(db.String(200))
    precio=db.Column(db.Float)
    detalles = db.relationship('DetallePedidos', backref='pizza', lazy=True)

class Clientes(db.Model):
    __tablename__='clientes'
    id_cliente=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100))
    direccion=db.Column(db.String(200))
    telefono=db.Column(db.String(20))
    pedidos = db.relationship('Pedidos', backref='cliente', lazy=True)

class Pedidos(db.Model):
    __tablename__='pedidos'
    id_pedido=db.Column(db.Integer, primary_key=True)
    id_cliente=db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'))
    fecha=db.Column(db.DateTime)
    total=db.Column(db.Float)
    detalles = db.relationship('DetallePedidos', backref='pedido', lazy=True)

class DetallePedidos(db.Model):
    __tablename__='detalle_pedidos'
    id_detalle=db.Column(db.Integer, primary_key=True)
    id_pedido=db.Column(db.Integer, db.ForeignKey('pedidos.id_pedido'))
    id_pizza=db.Column(db.Integer, db.ForeignKey('pizzas.id_pizza'))
    cantidad=db.Column(db.Integer)
    subtotal=db.Column(db.Float)