import functools
from flask import (
    render_template,
    Blueprint,
    flash,
    g,
    redirect,
    request,
    session,
    url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from administracionturquesas.models.usuario import Usuario
from administracionturquesas import db


auth = Blueprint('auth', __name__, url_prefix='/auth')

# Login
@auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        telefono = request.form.get('userName')
        password = request.form.get('password')

        error = None
        user = Usuario.query.filter_by(telefono=telefono).first()
        if user == None:
            error = 'Telefono o Password es incorrecto'
        elif not check_password_hash(user.password, password):
            error = 'Telefono o Password es incorrecto'
        elif user.esMoroso:
            error = 'Esta registrado como moroso, contacte a su comite'
        
        if error is None:
            session.clear()
            session['user_id'] = user.id   
            session.permanent = False
            if user.esPrimeraVez and user.idPrivada < 18:
                return redirect(url_for('auth.cambiarPassword'))
            elif user.idPrivada == 18:
                return redirect(url_for('admin.registrarAdministradores'))
            else:      
                return redirect(url_for('admin.index'))
           
        else:
            flash(error)
            return render_template('auth/login.html')
    else:
        if g.user:                      
            return redirect(url_for('admin.index'))           
        else:
            return render_template('auth/login.html')    


@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = Usuario.query.filter_by(id=user_id).first()     

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

# Login
@auth.route('/cambiarpassword', methods=('GET', 'POST'))
def cambiarPassword():
    if request.method == 'POST':
        password2 = request.form.get('password2')
        password = request.form.get('password')

        error = None
        if password == password2:
            user = Usuario.query.filter_by(id=g.user.id).first()
            user.password = generate_password_hash(password)
            user.esPrimeraVez = False
            db.session.add(user)
            db.session.commit()
            error = None            
        else:
            error = 'Passwords son diferentes'
        
        if error is not None:
            flash(error)
            return render_template('auth/cambiarpassword.html')
        else:
            session.clear()
            return redirect(url_for('auth.login')) 
    else:
        if not g.user:                                    
            return render_template('auth/login.html')  
        return render_template('auth/cambiarpassword.html') 