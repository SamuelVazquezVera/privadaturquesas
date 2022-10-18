
from flask import (
    render_template,
    Blueprint,
    flash,
    g,
    redirect,
    request,
    url_for
)

from administracionturquesas.models.usuario import Privada, Usuario, Visita, Pase
from administracionturquesas import db
from datetime import date, timedelta

seguridad = Blueprint('seguridad', __name__)


@seguridad.route("/index")
def index():
    return render_template('admin/index.html')


@seguridad.route("/visitantes", methods=('GET', 'POST'))
def verVisitantes():
    if g.user and g.user.esSeguridad:
        today = date.today()
        
        if request.method == 'POST':
            casa = request.form.get('vivienda')
            priv = request.form.get('privada')
            calle = request.form.get('calle')
            if casa is None:
                casa = ''

            if not casa.isdigit() and not priv.isdigit():
                strsql = "select * from visitaproveedor where esProveedor = 0 and '{}' between fechainicio and fechafin".format(today)

                result = db.session.execute(strsql)
                lista = []
                for r in result:
                    visita = Visita(r[0], r[1], r[2], r[3], r[4],
                                    r[5], r[6], r[7])
                    lista.append(visita)

                return render_template('security/visitantes.html', visitantes=lista, get_user=get_user, get_privada=get_privada, get_calle = get_calle)

            elif casa.isdigit() and priv.isdigit():
                strsql = "select * from visitaproveedor where idPrivada = {} and esProveedor = 0 and vivienda = {} and '{}' between fechainicio and fechafin".format(
                    str(priv), str(casa), today)

                result = db.session.execute(strsql)
                lista = []
                for r in result:
                    visita = Visita(r[0], r[1], r[2], r[3], r[4],
                                    r[5], r[6], r[7])
                    lista.append(visita)

                return render_template('security/visitantes.html', visitantes=lista, get_user=get_user, get_privada=get_privada, get_calle = get_calle)

            elif casa.isdigit() and priv.isdigit() and calle.isdigit():
                strsql = "select * from visitaproveedor where idPrivada = {} and esProveedor = 0 and vivienda = {}  and calle = {} and '{}' between fechainicio and fechafin".format(
                    str(priv), str(casa), str(calle), today)

                result = db.session.execute(strsql)
                lista = []
                for r in result:
                    visita = Visita(r[0], r[1], r[2], r[3], r[4],
                                    r[5], r[6], r[7])
                    lista.append(visita)

                return render_template('security/visitantes.html', visitantes=lista, get_user=get_user, get_privada=get_privada, get_calle = get_calle)

            elif priv.isdigit():
                strsql = "select * from visitaproveedor where idPrivada = {} and esProveedor = 0 and '{}' between fechainicio and fechafin".format(
                    str(priv), today)

                result = db.session.execute(strsql)
                lista = []
                for r in result:
                    visita = Visita(r[0], r[1], r[2], r[3], r[4],
                                    r[5], r[6], r[7])
                    lista.append(visita)

                return render_template('security/visitantes.html', visitantes=lista, get_user=get_user, get_privada=get_privada, get_calle = get_calle)


        else:
            strsql = "select * from visitaproveedor where esProveedor = 0 and '{}' between fechainicio and fechafin".format(
                today)

            result = db.session.execute(strsql)
            lista = []
            for r in result:
                visita = Visita(r[0], r[1], r[2], r[3], r[4],
                                r[5], r[6], r[7])
                lista.append(visita)
            return render_template('security/visitantes.html', visitantes=lista, get_user=get_user, get_privada=get_privada, get_calle = get_calle)
    else:
        return redirect(url_for('admin.index'))

@seguridad.route("/proveedores", methods=('GET', 'POST'))
def verProveedores():
    if g.user and g.user.esSeguridad:
        today = date.today()
        
        if request.method == 'POST':
            casa = request.form.get('vivienda')
            priv = request.form.get('privada')
            calle = request.form.get('calle')

            if casa is None:
                casa = ''

            if not casa.isdigit() and not priv.isdigit():
                strsql = "select * from visitaproveedor where esProveedor = 1 and '{}' between fechainicio and fechafin".format(today)

                result = db.session.execute(strsql)
                lista = []
                for r in result:
                    visita = Visita(r[0], r[1], r[2], r[3], r[4],
                                    r[5], r[6], r[7])
                    lista.append(visita)

                return render_template('security/proveedores.html', visitantes=lista, get_user=get_user, get_privada=get_privada, get_calle = get_calle)

            elif casa.isdigit() and priv.isdigit():
                strsql = "select * from visitaproveedor where idPrivada = {} and esProveedor = 1 and vivienda = {} and '{}' between fechainicio and fechafin".format(
                    str(priv), str(casa), today)

                result = db.session.execute(strsql)
                lista = []
                for r in result:
                    visita = Visita(r[0], r[1], r[2], r[3], r[4],
                                    r[5], r[6], r[7])
                    lista.append(visita)

                return render_template('security/proveedores.html', visitantes=lista, get_user=get_user, get_privada=get_privada, get_calle = get_calle)

            elif casa.isdigit() and priv.isdigit() and calle.isdigit():
                strsql = "select * from visitaproveedor where idPrivada = {} and esProveedor = 1 and vivienda = {}  and calle = {} and '{}' between fechainicio and fechafin".format(
                    str(priv), str(casa), str(calle), today)

                result = db.session.execute(strsql)
                lista = []
                for r in result:
                    visita = Visita(r[0], r[1], r[2], r[3], r[4],
                                    r[5], r[6], r[7])
                    lista.append(visita)

                return render_template('security/proveedores.html', visitantes=lista, get_user=get_user, get_privada=get_privada, get_calle = get_calle)

            elif priv.isdigit():
                strsql = "select * from visitaproveedor where idPrivada = {} and esProveedor = 1 and '{}' between fechainicio and fechafin".format(
                    str(priv), today)

                result = db.session.execute(strsql)
                lista = []
                for r in result:
                    visita = Visita(r[0], r[1], r[2], r[3], r[4],
                                    r[5], r[6], r[7])
                    lista.append(visita)

                return render_template('security/proveedores.html', visitantes=lista, get_user=get_user, get_privada=get_privada, get_calle = get_calle)

        else:
            strsql = "select * from visitaproveedor where esProveedor = 1 and '{}' between fechainicio and fechafin".format(
                today)

            result = db.session.execute(strsql)
            lista = []
            for r in result:
                visita = Visita(r[0], r[1], r[2], r[3], r[4],
                                r[5], r[6], r[7])
                lista.append(visita)
            return render_template('security/proveedores.html', visitantes=lista, get_user=get_user, get_privada=get_privada, get_calle = get_calle)
    else:
        return redirect(url_for('admin.index'))


@seguridad.route("/pasesES", methods=('GET', 'POST'))
def verPasesES():
    if g.user and g.user.esSeguridad:
        today = date.today()
        
        if request.method == 'POST':
            casa = request.form.get('vivienda')
            priv = request.form.get('privada')
            calle = request.form.get('calle')
            if casa is None:
                casa = ''

            if not casa.isdigit() and not priv.isdigit():
                strsql = "select * from pasees where '{}' between fechainicio and fechafin".format(today)

                result = db.session.execute(strsql)
                lista = []
                for r in result:
                    pase = Pase(r[0], r[1], r[2], r[3], r[4],
                                r[5], r[6], r[7], r[8], r[9])
                    lista.append(pase)

                return render_template('security/paseses.html', pases=lista, get_user=get_user, get_privada=get_privada, get_calle = get_calle)

            elif casa.isdigit() and priv.isdigit():
                strsql = "select * from pasees where idPrivada = {} and vivienda = {} and '{}' between fechainicio and fechafin".format(
                    str(priv), str(casa), today)

                result = db.session.execute(strsql)
                lista = []
                for r in result:
                    pase = Pase(r[0], r[1], r[2], r[3], r[4],
                                r[5], r[6], r[7], r[8], r[9])
                    lista.append(pase)

                return render_template('security/paseses.html', pases=lista, get_user=get_user, get_privada=get_privada, get_calle = get_calle)

            elif casa.isdigit() and priv.isdigit() and calle.isdigit():
                strsql = "select * from pasees where idPrivada = {} and vivienda = {}  and calle = {} and '{}' between fechainicio and fechafin".format(
                    str(priv), str(casa), str(calle), today)

                result = db.session.execute(strsql)
                lista = []
                for r in result:
                    pase = Pase(r[0], r[1], r[2], r[3], r[4],
                                r[5], r[6], r[7], r[8], r[9])
                    lista.append(pase)

                return render_template('security/paseses.html', pases=lista, get_user=get_user, get_privada=get_privada, get_calle = get_calle)

            elif priv.isdigit():
                strsql = "select * from pasees where idPrivada = {} and '{}' between fechainicio and fechafin".format(
                    str(priv), today)

                result = db.session.execute(strsql)
                lista = []
                for r in result:
                    pase = Pase(r[0], r[1], r[2], r[3], r[4],
                                r[5], r[6], r[7], r[8], r[9])
                    lista.append(pase)

                return render_template('security/paseses.html', pases=lista, get_user=get_user, get_privada=get_privada, get_calle = get_calle)


        else:
            strsql = "select * from pasees where '{}' between fechainicio and fechafin".format(today)

            result = db.session.execute(strsql)
            lista = []
            for r in result:
                    pase = Pase(r[0], r[1], r[2], r[3], r[4],
                                r[5], r[6], r[7], r[8], r[9])
                    lista.append(pase)
            return render_template('security/paseses.html', pases=lista, get_user=get_user, get_privada=get_privada, get_calle = get_calle)
    else:
        return redirect(url_for('admin.index'))


# Obtner un ususario


def get_user(id):
    user = Usuario.query.get_or_404(id)
    return user

# Obtner privada


def get_privada(id):
    privada = Privada.query.get_or_404(id)
    return privada


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
