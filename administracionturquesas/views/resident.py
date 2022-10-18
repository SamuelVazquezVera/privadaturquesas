from flask import (
    render_template,
    Blueprint,
    flash,
    g,
    redirect,
    request,
    url_for
)

from administracionturquesas.models.usuario import Privada, Usuario, Visita, VisitaProveedor
from administracionturquesas import db
from datetime import date, datetime, timedelta

resident = Blueprint('resident', __name__)


@resident.route("/index")
def index():
    return render_template('admin/index.html')


@resident.route("/registrarproveedor", methods=('GET', 'POST'))
def registrarProveedor():

    privada = Privada.query.filter_by(id=g.user.idPrivada).first()
    if request.method == 'POST':
        esProveedor = True
        nombre = request.form.get('nombre')
        idPrivada = g.user.idPrivada
        vivienda = g.user.vivienda
        calle = g.user.calle
        fechaInicio = request.form.get('finicio')
        fechaFin = request.form.get('ffin')

        fecha = datetime.strptime(fechaInicio, '%Y-%m-%d')
        fecha2 = datetime.strptime(fechaFin, '%Y-%m-%d')

        if fecha2 < fecha:
            flash('La fecha fin es menor a la fecha inicio')
            return render_template('resident/registrarproveedor.html', privada=privada)

        if calle is None:
            calle = ''

        visitaproveedor = VisitaProveedor(
            nombre, idPrivada, vivienda, fechaInicio, fechaFin, calle, g.user.id, esProveedor)
        db.session.add(visitaproveedor)
        db.session.commit()
        flash('Proveedor registrado')
        return render_template('resident/registrarproveedor.html', privada=privada)

    else:

        if g.user and not g.user.esAdministrador and not g.user.esMoroso:
            return render_template('resident/registrarproveedor.html', privada=privada)
        elif g.user and not g.user.esSeguridad and not g.user.esMoroso:
            return render_template('resident/registrarproveedor.html', privada=privada)
        else:
            return redirect(url_for('admin.index'))


@resident.route("/registrarvisita", methods=('GET', 'POST'))
def registrarVisita():

    privada = Privada.query.filter_by(id=g.user.idPrivada).first()
    if request.method == 'POST':
        esProveedor = False
        nombre = request.form.get('nombre')
        idPrivada = g.user.idPrivada
        vivienda = g.user.vivienda
        calle = g.user.calle
        fechaInicio = request.form.get('finicio')
        fechaFin = request.form.get('ffin')
        fecha = datetime.strptime(fechaInicio, '%Y-%m-%d')
        fecha2 = datetime.strptime(fechaFin, '%Y-%m-%d')

        if fecha2 < fecha:
            flash('La fecha fin es menor a la fecha inicio')
            return render_template('resident/registrarvisita.html', privada=privada)

        if calle is None:
            calle = ''

        visitaproveedor = VisitaProveedor(
            nombre, idPrivada, vivienda, fechaInicio, fechaFin, calle, g.user.id, esProveedor)
        db.session.add(visitaproveedor)
        db.session.commit()
        flash('Visita registrada')
        return render_template('resident/registrarvisita.html', privada=privada)

    else:

        if g.user and not g.user.esAdministrador and not g.user.esMoroso:
            return render_template('resident/registrarvisita.html', privada=privada)
        elif g.user and not g.user.esSeguridad and not g.user.esMoroso:
            return render_template('resident/registrarvisita.html', privada=privada)
        else:
            return redirect(url_for('admin.index'))


@resident.route("/actualizarvisita/<int:id>", methods=('GET', 'POST'))
def actualizarVisita(id):
    privada = Privada.query.filter_by(id=g.user.idPrivada).first()
    visita = VisitaProveedor.query.filter_by(
        id=id).filter_by(esProveedor=False).first()

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        fechaInicio = request.form.get('finicio')
        fechaFin = request.form.get('ffin')

        visita.nombre = nombre
        visita.fechainicio = fechaInicio
        visita.fechafin = fechaFin

        db.session.add(visita)
        db.session.commit()
        flash('Visita actualizada')
        visita = VisitaProveedor.query.filter_by(
            id=id).filter_by(esProveedor=False).first()
        return render_template('resident/actualizarvisita.html', visita=visita, privada=privada)

    else:
        if g.user and not g.user.esAdministrador and not g.user.esMoroso:
            return render_template('resident/actualizarvisita.html', visita=visita, privada=privada)
        elif g.user and not g.user.esSeguridad and not g.user.esMoroso:
            return render_template('resident/actualizarvisita.html', visita=visita, privada=privada)
        else:
            return redirect(url_for('admin.index'))


@resident.route("/actualizarproveedor/<int:id>", methods=('GET', 'POST'))
def actualizarProveedor(id):
    privada = Privada.query.filter_by(id=g.user.idPrivada).first()
    visita = VisitaProveedor.query.filter_by(
        id=id).filter_by(esProveedor=True).first()
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        fechaInicio = request.form.get('finicio')
        fechaFin = request.form.get('ffin')

        visita.nombre = nombre
        visita.fechainicio = fechaInicio
        visita.fechafin = fechaFin

        db.session.add(visita)
        db.session.commit()
        flash('Proveedor actualizado')
        visita = VisitaProveedor.query.filter_by(
            id=id).filter_by(esProveedor=True).first()
        return render_template('resident/actualizarproveedor.html', proveedor=visita, privada=privada)

    else:
        if g.user and not g.user.esAdministrador and not g.user.esMoroso:
            return render_template('resident/actualizarproveedor.html', proveedor=visita, privada=privada)
        elif g.user and not g.user.esSeguridad and not g.user.esMoroso:
            return render_template('resident/actualizarproveedor.html', proveedor=visita, privada=privada)
        else:
            return redirect(url_for('admin.index'))


@resident.route("/vervisitas")
def verVisitas():
    if g.user:
        privada = Privada.query.filter_by(id=g.user.idPrivada).first()

    if g.user and not g.user.esAdministrador and not g.user.esMoroso:
        today = date.today()
        td = timedelta(5)
        todayAfter = today + td

        strsql = "select * from visitaproveedor where idPrivada = {} and esProveedor = 0 and vivienda = {} and calle = '{}' and (fechainicio >= '{}' or fechafin <= '{}')".format(
            str(g.user.idPrivada), str(g.user.vivienda), g.user.calle, today, todayAfter)

        result = db.session.execute(strsql)
        lista = []
        for r in result:
            visita = Visita(r[0], r[1], r[2], r[3], r[4],
                            r[5], r[6], r[7])
            lista.append(visita)
        return render_template('resident/vervisitas.html', visitas=lista, privada=privada, get_user=get_user, get_calle = get_calle)
    elif g.user and not g.user.esSeguridad and not g.user.esMoroso:
        today = date.today()
        td = timedelta(5)
        todayAfter = today + td

        strsql = "select * from visitaproveedor where idPrivada = {} and esProveedor = 0 and vivienda = {} and calle = '{}' and (fechainicio >= '{}' or fechafin <= '{}')".format(
            str(g.user.idPrivada), str(g.user.vivienda), g.user.calle, today, todayAfter)

        result = db.session.execute(strsql)
        lista = []
        for r in result:
            visita = Visita(r[0], r[1], r[2], r[3], r[4],
                            r[5], r[6], r[7])
            lista.append(visita)
        return render_template('resident/vervisitas.html', visitas=lista, privada=privada, get_user=get_user, get_calle = get_calle)
    else:
        return redirect(url_for('admin.index'))

@resident.route("/verproveedores")
def verProveedores():
    if g.user:
        privada = Privada.query.filter_by(id=g.user.idPrivada).first()

    if g.user and not g.user.esAdministrador and not g.user.esMoroso:
        today = date.today()
        td = timedelta(5)
        todayAfter = today + td

        strsql = "select * from visitaproveedor where idPrivada = {} and esProveedor = 1 and vivienda = {} and calle = '{}' and (fechainicio >= '{}' or fechafin <= '{}')".format(
            str(g.user.idPrivada), str(g.user.vivienda), g.user.calle, today, todayAfter)

        result = db.session.execute(strsql)
        lista = []
        for r in result:
            visita = Visita(r[0], r[1], r[2], r[3], r[4],
                            r[5], r[6], r[7])
            lista.append(visita)
        return render_template('resident/verproveedores.html', proveedores=lista, privada=privada, get_user=get_user, get_calle = get_calle)
    elif g.user and not g.user.esSeguridad and not g.user.esMoroso:
        today = date.today()
        td = timedelta(5)
        todayAfter = today + td

        strsql = "select * from visitaproveedor where idPrivada = {} and esProveedor = 1 and vivienda = {} and calle = '{}' and (fechainicio >= '{}' or fechafin <= '{}')".format(
            str(g.user.idPrivada), str(g.user.vivienda), g.user.calle, today, todayAfter)

        result = db.session.execute(strsql)
        lista = []
        for r in result:
            visita = Visita(r[0], r[1], r[2], r[3], r[4],
                            r[5], r[6], r[7])
            lista.append(visita)
        return render_template('resident/verproveedores.html', proveedores=lista, privada=privada, get_user=get_user, get_calle = get_calle)
    else:
        return redirect(url_for('admin.index'))

# Obtner un ususario
def get_user(id):
    user = Usuario.query.filter_by(id = id).first()
    return user

def get_calle(id):
    calle = ''
    if id == '1':
        return 'Agua Grande'
    elif id == '2':
        return 'Chautengo'
    elif id == '3':
        return 'Cuyutlan'
    elif id == '4':
        return 'Mitla'
    elif id == '5':
        return 'Chavel'
    elif id == '6':
        return 'Brizola'
    elif id == '7':
        return 'Yalca'
    elif id == '8':
        return 'Zempoala'

    return calle
