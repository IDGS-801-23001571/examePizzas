from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db

from pedidos.routes import pedidos
from historial.routes import historial

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

app.register_blueprint(pedidos, url_prefix='/pedidos')
app.register_blueprint(historial, url_prefix='/historial')

db.init_app(app)

csrf = CSRFProtect()

@app.route('/')
def home():
    return render_template("home.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True) 