from administracionturquesas import db

class Privada(db.Model):
    __tablename__ = 'privada'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))

    def __init__(self, id) -> None:
        self.id = id

    def __repr__(self) -> None:
        return f'Privada: {self.nombre}'

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    password = db.Column(db.Text, nullable=False)
    telefono = db.Column(db.String(10), nullable=False)
    esPrimeraVez = db.Column(db.Boolean, unique=False, default=True)
    esAdministrador = db.Column(db.Boolean, unique=False, default=False)
    esMoroso = db.Column(db.Boolean, unique=False, default=False)
    esSeguridad = db.Column(db.Boolean, unique=False, default=False)
    calle = db.Column(db.Integer, nullable=False)
    idPrivada = db.Column(db.Integer, db.ForeignKey(
        'privada.id'), nullable=False)
    vivienda = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(200), nullable=False)

    privada = db.relationship('Privada')

    def __init__(self, nombre, password, telefono, esPrimeraVez, esAdministrador, esMoroso, esSeguridad, calle, idPrivada, vivienda, email) -> None:
        self.nombre = nombre
        self.telefono = telefono
        self.password = password
        self.esPrimeraVez = esPrimeraVez
        self.esAdministrador = esAdministrador
        self.esMoroso = esMoroso
        self.esSeguridad = esSeguridad
        self.calle = calle
        self.idPrivada = idPrivada
        self.vivienda = vivienda
        self.email = email

    def __repr__(self) -> str:
        return f''

class PaseES(db.Model):
    __tablename__ = 'pasees'
    id = db.Column(db.Integer, primary_key=True)
    nombrepropietario = db.Column(db.String(200))
    idPrivada = db.Column(db.Integer, db.ForeignKey(
        'privada.id'), nullable=False)
    vivienda = db.Column(db.Integer, nullable=False)
    movimiento = db.Column(db.String(200))
    fechainicio = db.Column(db.Date, nullable=False)
    fechafin = db.Column(db.Date, nullable=False)
    calle = db.Column(db.Integer, nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey(
        'usuario.id'), nullable=False)
    moroso = db.Column(db.Boolean, unique=False, default=False)

    privada = db.relationship('Privada')
    usuario = db.relationship('Usuario')

    def __init__(self, nombrepropietario, idPrivada, vivienda, movimiento, fechainicio, fechafin, calle, idusuario, moroso) -> None:
        self.nombrepropietario = nombrepropietario
        self.idPrivada = idPrivada
        self.vivienda = vivienda
        self.movimiento = movimiento
        self.fechainicio = fechainicio
        self.fechafin = fechafin
        self.calle = calle
        self.idUsuario = idusuario
        self.moroso = moroso

    def __repr__(self) -> None:
        return f'Privada: {self.nombre}'

class VisitaProveedor(db.Model):
    __tablename__ = 'visitaproveedor'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    idPrivada = db.Column(db.Integer, db.ForeignKey(
        'privada.id'), nullable=False)
    calle = db.Column(db.Integer, nullable=False)
    vivienda = db.Column(db.Integer, nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey(
        'usuario.id'), nullable=False)
    fechainicio = db.Column(db.Date, nullable=False)
    fechafin = db.Column(db.Date, nullable=False)
    esProveedor = db.Column(db.Boolean, unique=False, default=False)

    privada = db.relationship('Privada')
    usuario = db.relationship('Usuario')

    def __init__(self, nombre, idPrivada, vivienda, fechainicio, fechafin, calle, idusuario, esProveedor) -> None:
        self.nombre = nombre
        self.idPrivada = idPrivada
        self.vivienda = vivienda
        self.fechainicio = fechainicio
        self.fechafin = fechafin
        self.calle = calle
        self.idUsuario = idusuario
        self.esProveedor = esProveedor

    def __repr__(self) -> None:
        return f'Privada: {self.nombre}'

class Pase:
    def __init__(self, id, nombrepropietario, idPrivada, vivienda, movimiento, fechainicio, fechafin, calle, idUsuario, moroso):
        self.id = id
        self.nombrepropietario = nombrepropietario
        self.idPrivada = idPrivada
        self.vivienda = vivienda
        self.movimiento = movimiento
        self.fechainicio = fechainicio
        self.fechafin = fechafin
        self.calle = calle
        self.idUsuario = idUsuario
        self.moroso = moroso

class Visita:

    def __init__(self, id, nombre, idPrivada, calle, vivienda, idUsuario, fechainicio, fechafin):
        self.id = id
        self.nombre = nombre
        self.idPrivada = idPrivada
        self.calle = calle
        self.vivienda = vivienda
        self.idUsuario = idUsuario
        self.fechainicio = fechainicio
        self.fechafin = fechafin

class Priv:

    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre