from datetime import datetime
from flask import (
    render_template,
    Blueprint,
    flash,
    g,
    redirect,
    request,
    url_for
)

from administracionturquesas.models.usuario import Privada, Usuario, Pase
from administracionturquesas.models.usuario import PaseES
from administracionturquesas import db
from datetime import date, timedelta
from werkzeug.security import generate_password_hash

admin = Blueprint('admin', __name__)


@admin.route("/index")
def index():
    return render_template('admin/index.html')

@admin.route("/registraradministradores", methods=('GET', 'POST'))
def registrarAdministradores():    
    if request.method == 'POST':
        moroso = False
        administrador = False
        seguridad = False

        nombrePropietario = request.form.get('nombre')
        password = generate_password_hash("123456")
        telefono = request.form.get('telefono')
        esPrimeraVez = True
        vivienda = request.form.get('vivienda')
        email = request.form.get('email')
        calle = request.form.get('calle')
        tipousuario = request.form.get('tipousuario')    
        privada = request.form.get('privada')      

        if privada == 'privada':
            flash('Favor de seleccionar una privada')        
            return render_template('auth/administrador.html')

        if calle is None:
            calle = 0
        if email is None:
            email = ''
        
        if tipousuario == 'seguridad':
            administrador = False
            seguridad = True
        elif tipousuario == 'administrador':
            administrador = True

        user = Usuario(nombrePropietario, password, telefono, esPrimeraVez,
                       administrador, moroso, seguridad, calle, privada, vivienda, email)
        db.session.add(user)
        db.session.commit()
        flash('Usuario agregado')
        
        return render_template('auth/administrador.html')
    else:
        if g.user:            
            return render_template('auth/administrador.html')
        else:
            return render_template('admin/index.html')


@admin.route("/registrarusuario", methods=('GET', 'POST'))
def registrarUsuario():
    if request.method == 'POST':
        moroso = False
        administrador = False
        seguridad = False

        nombrePropietario = request.form.get('nombre')
        password = generate_password_hash("123456")
        telefono = request.form.get('telefono')
        esPrimeraVez = True
        vivienda = request.form.get('vivienda')
        email = request.form.get('email')
        calle = request.form.get('calle')
        tipousuario = request.form.get('tipousuario')
        esMoroso = request.form.get('moroso')

        if calle is None:
            calle = 0
        if email is None:
            email = ''
        if esMoroso is None:
            moroso = False
        else:
            moroso = True
        if tipousuario == 'seguridad':
            administrador = False
            seguridad = True
        elif tipousuario == 'administrador':
            administrador = True

        user = Usuario(nombrePropietario, password, telefono, esPrimeraVez,
                       administrador, moroso, seguridad, calle, g.user.idPrivada, vivienda, email)
        db.session.add(user)
        db.session.commit()
        flash('Usuario agregado')
        privada = Privada.query.filter_by(id=g.user.idPrivada).first()
        return render_template('admin/registrarusuario.html', privada=privada)
    else:
        if g.user and g.user.esAdministrador:
            privada = Privada.query.filter_by(id=g.user.idPrivada).first()
            return render_template('admin/registrarusuario.html', privada=privada)
        else:
            return render_template('admin/index.html')


@admin.route("/registrarpase", methods=('GET', 'POST'))
def registrarPase():
    if request.method == 'POST':
        moroso = False
        nombrePropietario = request.form.get('nombre')
        idPrivada = g.user.idPrivada
        vivienda = request.form.get('vivienda')
        movimiento = request.form.get('movimiento')
        calle = request.form.get('calle')
        fechaInicio = request.form.get('finicio')
        fechaFin = request.form.get('ffin')
        esMoroso = request.form.get('moroso')

        fecha = datetime.strptime(fechaInicio, '%Y-%m-%d')
        fecha2 = datetime.strptime(fechaFin, '%Y-%m-%d')

        if fecha2 < fecha:
            flash('La fecha fin es menor a la fecha inicio')
            privada = Privada.query.filter_by(id=g.user.idPrivada).first()
            return render_template('admin/registrarpase.html', privada=privada)


        if calle is None:
            calle = ''
        if esMoroso is None:
            moroso = False
        else:
            moroso = True

        pase = PaseES(nombrePropietario, idPrivada, vivienda,
                      movimiento, fechaInicio, fechaFin, calle, g.user.id, moroso)

        db.session.add(pase)
        db.session.commit()
        return redirect(url_for('admin.verPase'))

    else:
        if g.user and g.user.esAdministrador:
            privada = Privada.query.filter_by(id=g.user.idPrivada).first()
            return render_template('admin/registrarpase.html', privada=privada)
        else:
            return render_template('admin/index.html')


@admin.route("/verpase")
def verPase():
    if g.user and g.user.esAdministrador:
        today = date.today()
        td = timedelta(5)
        todayAfter = today + td

        privada = Privada.query.filter_by(id=g.user.idPrivada).first()

        strsql = "select * from pasees where idPrivada = {} and (fechainicio >= '{}' or fechafin <= '{}')".format(
            str(g.user.idPrivada), today, todayAfter)

        result = db.session.execute(strsql)
        lista = []
        for r in result:
            pase = Pase(r[0], r[1], r[2], r[3], r[4],
                        r[5], r[6], r[7], r[8], r[9])
            lista.append(pase)

        return render_template('admin/verpase.html', pases=lista, privada=privada, get_user=get_user, get_calle = get_calle)
    else:
        return render_template('admin/index.html')

@admin.route("/verusuarios", methods=('GET', 'POST'))
def verUsuarios():
    if g.user and g.user.esAdministrador:
        privada = Privada.query.filter_by(id=g.user.idPrivada).first()
        if request.method == 'POST':
            casa =  request.form.get('vivienda')
                  
            if not casa.isdigit():
                usuarios = Usuario.query.filter_by(idPrivada=g.user.idPrivada).all()
                return render_template('admin/verusuarios.html', usuarios=usuarios, privada=privada, get_user=get_user, get_calle = get_calle)
            else:
                usuarios = Usuario.query.filter_by(idPrivada=g.user.idPrivada).filter_by(vivienda = casa).all()
                return render_template('admin/verusuarios.html', usuarios=usuarios, privada=privada, get_user=get_user, get_calle = get_calle)
        else:           
            usuarios = Usuario.query.filter_by(idPrivada=g.user.idPrivada).all()
            return render_template('admin/verusuarios.html', usuarios=usuarios, privada=privada, get_user=get_user, get_calle = get_calle)
    else:
        return render_template('admin/index.html')

@admin.route("/actualizarpase/<int:id>", methods=('GET', 'POST'))
def actualizarPase(id):

    if g.user and g.user.esAdministrador:
        pase = PaseES.query.filter_by(id=id).first()
        privada = Privada.query.filter_by(id=g.user.idPrivada).first()
        if request.method == 'POST':
            moroso = False
            nombrePropietario = request.form.get('nombre')
            idPrivada = g.user.idPrivada
            vivienda = request.form.get('vivienda')
            movimiento = request.form.get('movimiento')
            calle = request.form.get('calle')
            fechaInicio = request.form.get('finicio')
            fechaFin = request.form.get('ffin')
            esMoroso = request.form.get('moroso')

            if calle is None:
                calle = ''
            if esMoroso is None:
                moroso = False
            else:
                moroso = True

            pase.nombrepropietario = nombrePropietario
            pase.idPrivada = idPrivada
            pase.vivienda = vivienda
            pase.movimiento = movimiento
            pase.fechainicio = fechaInicio
            pase.fechafin = fechaFin
            pase.calle = calle
            pase.idUsuario = g.user.id
            pase.moroso = moroso

            db.session.add(pase)
            db.session.commit()
            flash('Pase actualizado')
            return render_template('admin/actualizarpase.html', pase=pase, privada=privada, get_calle = get_calle)
        else:
            return render_template('admin/actualizarpase.html', pase=pase, privada=privada, get_calle = get_calle)
    else:
        return render_template('admin/index.html')

@admin.route("/actualizarusuario/<int:id>", methods=('GET', 'POST'))
def actualizarUsuario(id):

    if g.user and g.user.esAdministrador:
        usuario = Usuario.query.filter_by(id=id).first()
        privada = Privada.query.filter_by(id=g.user.idPrivada).first()
        if request.method == 'POST':
            moroso = False
            administrador = False
            seguridad = False

            nombrePropietario = request.form.get('nombre')            
            telefono = request.form.get('telefono')            
            vivienda = request.form.get('vivienda')
            email = request.form.get('email')
            calle = request.form.get('calle')
            tipousuario = request.form.get('tipousuario')
            esMoroso = request.form.get('moroso')

            if calle is None:
                calle = ''
            if email is None:
                email = ''
            if esMoroso is None:
                moroso = False
            else:
                moroso = True
            if tipousuario == 'seguridad':
                administrador = False
                seguridad = True
            elif tipousuario == 'administrador':
                administrador = True

            usuario.nombre = nombrePropietario
            usuario.telefono = telefono
            usuario.esAdministrador = administrador
            usuario.esMoroso = moroso
            usuario.esSeguridad = seguridad
            usuario.calle = calle
            usuario.vivienda = vivienda
            usuario.email = email

            db.session.add(usuario)
            db.session.commit()
            flash('Usuario actualizado')
            return render_template('admin/actualizarusuario.html', usuario=usuario, privada=privada, get_calle = get_calle)
        else:
            return render_template('admin/actualizarusuario.html', usuario=usuario, privada=privada, get_calle = get_calle)
    else:
        return render_template('admin/index.html')

@admin.route("/eliminarpase/<int:id>", methods=('GET', 'POST'))
def eliminarPase(id):

    if g.user and g.user.esAdministrador:
        pase = PaseES.query.filter_by(id=id).first()
        db.session.delete(pase)
        db.session.commit()

        return  redirect(url_for('admin.verPase'))        

    else:
        return render_template('admin/index.html')

@admin.route("/eliminarusuario/<int:id>", methods=('GET', 'POST'))
def eliminarUsuario(id):

    if g.user and g.user.esAdministrador:
        usuario = Usuario.query.filter_by(id=id).first()
        db.session.delete(usuario)
        db.session.commit()

        return  redirect(url_for('admin.verUsuarios'))        

    else:
        return render_template('admin/index.html')

@admin.route("/resetearpassword/<int:id>", methods=('GET', 'POST'))
def resetearPass(id):

    if g.user and g.user.esAdministrador:
        usuario = Usuario.query.filter_by(id=id).first()
        privada = Privada.query.filter_by(id=g.user.idPrivada).first()

        if request.method == 'POST':
                  
            usuario.esPrimeraVez = True
            usuario.password = generate_password_hash("123456")
            db.session.add(usuario)
            db.session.commit()
            flash('Password reseteado')
            privada = Privada.query.filter_by(id=g.user.idPrivada).first()
            Usuario.query.filter_by(id=id).first()
            return render_template('admin/resetearpassword.html', usuario=usuario, privada=privada)            
        else:
            return render_template('admin/resetearpassword.html', usuario=usuario, privada=privada)
    else:
        return render_template('admin/index.html')        

# Obtner un ususario
def get_user(id):
    user = Usuario.query.get_or_404(id)
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

