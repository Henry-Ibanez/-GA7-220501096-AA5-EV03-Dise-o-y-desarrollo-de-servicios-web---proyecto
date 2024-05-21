from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        nombre = request.form['usuario']
        contraseña = request.form['password']
        
        # Consulta a la base de datos para autenticar al usuario
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE nombre = %s AND contraseña = %s", (nombre, contraseña))
        user = cur.fetchone()
        cur.close()

        if user:
            # Autenticación exitosa
            return redirect(url_for('admin_welcomeadmin'))
        else:
            # Autenticación fallida
            return "Usuario o contraseña incorrectos"
    else:
        return render_template('admin/login.html')

@app.route('/admin/welcomeadmin')
def admin_welcomeadmin():
    return render_template('admin/welcomeadmin.html')

if __name__ == '__main__':
    app.run(debug=True)
