from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'proyecto_api'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Inicialización de la extensión MySQL
mysql = MySQL(app)

# Configuración de la clave secreta para las sesiones (necesaria para el uso de sesiones en Flask)
app.secret_key = 'tu_clave_secreta'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None  # Inicializar el mensaje de error como None
    
    if request.method == 'POST':
        nombre = request.form['usuario']
        contraseña = request.form['password']
        
        # Consulta a la base de datos para autenticar al usuario
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE nombre = %s AND contraseña = %s", (nombre, contraseña))
        user = cur.fetchone()
        cur.close()

        if user:
            # Autenticación exitosa, establece el usuario en la sesión
            session['usuario'] = user['nombre']
            return redirect(url_for('admin_welcomeadmin'))
        else:
            # Autenticación fallida, establece el mensaje de error
            error = "Usuario o contraseña incorrectos"

    return render_template('admin/login.html', error=error)  # Pasa el mensaje de error a la plantilla

@app.route('/admin/welcomeadmin')
def admin_welcomeadmin():
    if 'usuario' in session:
        return render_template('admin/welcomeadmin.html')
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('usuario', None)  # Elimina el usuario de la sesión
    return redirect(url_for('index'))  # Redirige al usuario a la página de inicio

if __name__ == '__main__':
    app.run(debug=True)
