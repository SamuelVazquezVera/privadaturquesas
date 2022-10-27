from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=720)

#Cargar las configuraciones
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

#importar vistas
from administracionturquesas.views.auth import auth
from administracionturquesas.views.index import index
from administracionturquesas.views.admin import admin
from administracionturquesas.views.resident import resident
from administracionturquesas.views.seguridad import seguridad

app.register_blueprint(auth)
app.register_blueprint(index)
app.register_blueprint(admin)
app.register_blueprint(resident)
app.register_blueprint(seguridad)

db.init_app(app)
csrf.init_app(app)
with app.app_context():
    db.create_all()