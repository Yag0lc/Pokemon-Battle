from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from app.services.entrenador_service import comprobarEntrenador,registrarEntrenador


pokemons_bp_home = Blueprint('pokemons_bp_home', __name__)




# === RUTA PRINCIPAL ===
@pokemons_bp_home.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        nombre = request.form.get('trainer', '').strip()
        password = request.form.get('password', '').strip()

        if nombre and 3 <= len(nombre) <= 15:
            if comprobarEntrenador(nombre, password):
                session['trainer'] = nombre
                return redirect(url_for('pokemons_bp_lista.lista'))
            else:
                return render_template(
                    'Home.html',
                    errorNombre="Usuario o contraseña incorrectos"
                )

    if 'trainer' in session:
        return redirect(url_for('pokemons_bp_lista.lista'))

    return render_template('Home.html')

@pokemons_bp_home.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('trainer', '').strip()
        password = request.form.get('password', '').strip()

        if not (3 <= len(nombre) <= 15):
            return render_template('Register.html', errorNombre="El nombre debe tener entre 3 y 15 caracteres.")
        

        if len(password) < 3:
            return render_template('Register.html', errorNombre="La contraseña debe tener mínimo 3 caracteres.")

        entrenador = registrarEntrenador(nombre,password)
        if entrenador:
            return render_template('Home.html')


    return render_template('Register.html')

# === RUTA PARA CERRAR SESIÓN ===
@pokemons_bp_home.route('/logout')
def logout():
    session.pop('trainer', None)
    session.pop('pokemon_seleccionado', None)
    session.pop('batalla_actual', None)
    return redirect(url_for('pokemons_bp_home.home'))