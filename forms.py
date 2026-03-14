from wtforms import Form
from wtforms import StringField, IntegerField
from wtforms import validators

class PedidoForm(Form):
    nombre_cliente = StringField("nombre_cliente", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=2, max=100, message="Ingresa un nombre válido")
    ])

    direccion = StringField("direccion", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=2, max=200, message="Ingresa una dirección válida")
    ])

    telefono = StringField("telefono", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=10, max=12, message="Ingresa un teléfono válido")
    ])

    dia = IntegerField("dia", [
        validators.DataRequired(message="El campo es requerido"),
        validators.NumberRange(min=1, max=31, message="Seleccione un día válido")
    ])

    mes = IntegerField("mes", [
        validators.DataRequired(message="El campo es requerido"),
        validators.NumberRange(min=1, max=12, message="Seleccione un mes válido")
    ])

    anio = IntegerField("anio", [
        validators.DataRequired(message="El campo es requerido"),
        validators.NumberRange(min=2024, max=2100, message="Seleccione un año válido")
    ])

    tamano = StringField("tamano", [
        validators.DataRequired(message="El campo es requerido")
    ])

    ingredientes = StringField("ingredientes", [
        validators.DataRequired(message="El campo es requerido")
    ])

    num_pizzas = IntegerField("num_pizzas", [
        validators.DataRequired(message="El campo es requerido"),
        validators.NumberRange(min=1, max=50, message="Cantidad no válida")
    ])


class ConsultaForm(Form):
    dia = IntegerField("dia", [
        validators.DataRequired(message="El campo es requerido"),
        validators.NumberRange(min=1, max=31, message="Seleccione un día válido")
    ])

    mes = IntegerField("mes", [
        validators.DataRequired(message="El campo es requerido"),
        validators.NumberRange(min=1, max=12, message="Seleccione un mes válido")
    ])

    anio = IntegerField("anio", [
        validators.DataRequired(message="El campo es requerido"),
        validators.NumberRange(min=2024, max=2100, message="Seleccione un año válido")
    ])