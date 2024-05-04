from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import pandas as pd
from datetime import datetime

import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
# Registrar la segunda fuente
pdfmetrics.registerFont(TTFont('PoppinsRegular', 'domyclip-adm/static/Poppins-Regular.ttf'))
# Registrar la tercera fuente
pdfmetrics.registerFont(TTFont('PoppinsBold', 'domyclip-adm/static/Poppins-Bold.ttf'))


# Importa la función para obtener la fecha actual
def obtener_fecha_actual():
    return datetime.today().strftime("%Y-%m-%d")

app = Flask(__name__, static_url_path='/login')
app.secret_key = 'admin'  # Configura la clave secreta

# Redirigir la ruta base '/' a la página de inicio de sesión '/login'
@app.route('/')
def home():
    return redirect(url_for('login'))

# Configura la conexión a la base de datos SQLite
DATABASE = 'database.db'


# Simulación de una lista de números de pago válidos
numeros_de_pago_validos = ['123456789', '987654321', '555555555']

# Ruta para el pago del cliente
@app.route('/pago_cliente', methods=['GET', 'POST'])
@app.route('/pago_cliente/<numero_pago>', methods=['GET', 'POST'])
def pago_cliente(numero_pago=None):
    if request.method == 'POST':
        numero_pago_form = request.form['Numero_pago']
        valor_pago = request.form['valor_pago']
        fecha_pago = request.form['fecha_pago']
        documento_pago = request.files['documento_pago']

        # Validar si el número de pago existe en la lista de números de pago válidos
        if numero_pago_form not in numeros_de_pago_validos:
            error_message = "El número de pago no existe."
            return render_template('pagosCliente.html', numero_pago=numero_pago_form, error_message=error_message)
        else:
            # Aquí iría el código para procesar el formulario si el número de pago es válido
            # Por ejemplo, podrías almacenar los datos en una base de datos
            return "¡Pago registrado exitosamente!"

    # Si la solicitud no es POST, renderizamos el formulario con el número de pago de la URL, si está presente
    return render_template('pagosCliente.html', numero_pago=numero_pago, error_message="")


def agregar_usuario(username, email, password):
    # Verificar si ya existe un usuario con el mismo nombre de usuario o correo electrónico
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Usuarios WHERE username = ? OR correo = ?', (username, email))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        if existing_user[1] == username and existing_user[2] == email:
            return False, "El nombre de usuario y el correo electrónico ya están en uso."
        elif existing_user[1] == username:
            return False, "El nombre de usuario ya está en uso."
        else:
            return False, "El correo electrónico ya está en uso."
    else:
        cursor.execute('INSERT INTO Usuarios (username, correo, password) VALUES (?, ?, ?)', (username, email, password))
        conn.commit()
        conn.close()
        return True, None  # Usuario agregado correctamente, sin errores


def obtener_usuario(username, email):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Usuarios WHERE username = ? AND correo = ?', (username, email))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

# Función para verificar credenciales
def check_credentials(username, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Usuarios WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_error = None
    registro_error = None

    if request.method == 'POST':
        if request.form.get('registro') == 'registro':
            # Registro de nuevos usuarios
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            success, error_message = agregar_usuario(username, email, password)
            if success:
                session['username'] = username
                return redirect('/login')  # Redirigir a la página de inicio después del registro
            else:
                registro_error = error_message

        else:
            # Inicio de sesión
            username = request.form['username']
            password = request.form['password']
            if check_credentials(username, password):
                session['username'] = username
                return redirect('/indexEdi')  # Redirigir a la página de inicio después de iniciar sesión
            else:
                login_error = 'Usuario o contraseña incorrectos'
    
    return render_template('login.html', login_error=login_error, registro_error=registro_error)

# Ruta para manejar la creación y el almacenamiento de la configuración del edificio
@app.route('/crear_configuracion_edificio', methods=['POST'])
def crear_configuracion_edificio():
    if request.method == 'POST':
        # Obtener los datos del formulario
        usuario_id = request.form['usuario_id']
        edificio_id = request.form['edificio_id']
        nombre = request.form['nombre']
        apartamentos = request.form['apartamentos']
        direccion = request.form['direccion']
        porteria = request.form['porteria']
        nit = request.form['nit']
        porcentaje = request.form['porcentaje']
        Banco1 = request.form['Banco1']
        Banco2 = request.form['Banco2']
        Banco3 = request.form['Banco3']
        Banco4 = request.form['Banco4']
        Banco5 = request.form['Banco5']
        estrucRC1 = request.form['estrucRC1']
        estrucRC2 = request.form['estrucRC2']
        estrucRC3 = request.form['estrucRC3']
        estrucRC4 = request.form['estrucRC4']
        estrucRC5 = request.form['estrucRC5']
        estrucRC6 = request.form['estrucRC6']
        estrucRC7 = request.form['estrucRC7']

        # Insertar los datos en la base de datos
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Edificios (usuario_id, edificio_id, nombre, apartamentos, direccion, porteria, nit,
                                   porcentaje, Banco1, Banco2, Banco3, Banco4, Banco5, estrucRC1, estrucRC2,
                                   estrucRC3, estrucRC4, estrucRC5, estrucRC6, estrucRC7)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (usuario_id, edificio_id, nombre, apartamentos, direccion, porteria, nit, porcentaje, Banco1,
              Banco2, Banco3, Banco4, Banco5, estrucRC1, estrucRC2, estrucRC3, estrucRC4, estrucRC5, estrucRC6, estrucRC7))
        conn.commit()
        conn.close()

        return redirect('/indexEdi')
    
@app.route('/guardar_configuracion_edificio', methods=['POST'])
def guardar_configuracion_edificio():
    if request.method == 'POST':
        # Obtener los datos del formulario
        edificio_id = request.form['edificio_id']
        nombre = request.form['nombre-edificio']
        telefono_porteria = request.form['telefono-porteria']
        direccion = request.form['direccion']
        nit = request.form['nit']
        porcentaje_interes = request.form['porcentaje-interes']

        # Actualizar los datos en la base de datos
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Edificios 
            SET nombre=?, porteria=?, direccion=?, nit=?, porcentaje=?
            WHERE edificio_id=? 
        ''', (nombre, telefono_porteria, direccion, nit, porcentaje_interes, edificio_id))
        conn.commit()
        conn.close()

        # Después de guardar los datos, redirige a donde sea necesario
        return redirect(f'/configuracion/{edificio_id}/')
    
@app.route('/guardar_configuracion_bancos', methods=['POST'])
def guardar_configuracion_bancos():
    if request.method == 'POST':
        # Obtener los datos del formulario
        edificio_id = request.form['edificio_id']
        banco1 = request.form['banco1']
        banco1_num = request.form['banco1_num']
        banco1_tipo = request.form['banco1_tipo']
        banco2 = request.form['banco2']
        banco2_num = request.form['banco2_num']
        banco2_tipo = request.form['banco2_tipo']
        banco3 = request.form['banco3']
        banco3_num = request.form['banco3_num']
        banco3_tipo = request.form['banco3_tipo']
        banco4 = request.form['banco4']
        banco4_num = request.form['banco4_num']
        banco4_tipo = request.form['banco4_tipo']

        # Actualizar los datos en la base de datos
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Edificios 
            SET Banco1=?, Cuenta1=?, tipo1=?,
                Banco2=?, Cuenta2=?, tipo2=?,
                Banco3=?, Cuenta3=?, tipo3=?,
                Banco4=?, Cuenta4=?, tipo4=?
            WHERE edificio_id=?
        ''', (banco1, banco1_num, banco1_tipo,
              banco2, banco2_num, banco2_tipo,
              banco3, banco3_num, banco3_tipo,
              banco4, banco4_num, banco4_tipo,
              edificio_id))
        conn.commit()
        conn.close()

        # Después de guardar los datos, redirige a donde sea necesario
        return redirect(f'/configuracion/{edificio_id}/')

    
@app.route('/guardar_configuracion_estructura', methods=['POST'])
def guardar_configuracion_estructura():
    if request.method == 'POST':
        edificio_id = request.form['edificio_id']
        estrucRC1 = request.form['estrucRC1']
        estrucRC2 = request.form['estrucRC2']
        estrucRC3 = request.form['estrucRC3']
        estrucRC4 = request.form['estrucRC4']
        estrucRC5 = request.form['estrucRC5']
        estrucRC6 = request.form['estrucRC6']
        estrucRC7 = request.form['estrucRC7']

        # Actualizar los datos en la base de datos
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Edificios 
            SET estrucRC1=?, estrucRC2=?, estrucRC3=?, estrucRC4=?, estrucRC5=?, estrucRC6=?, estrucRC7=?
            WHERE edificio_id=?
        ''', (estrucRC1, estrucRC2, estrucRC3, estrucRC4, estrucRC5, estrucRC6, estrucRC7, edificio_id))
        conn.commit()
        conn.close()

        return redirect(f'/configuracion/{edificio_id}/')



# Ruta del editor después del inicio de sesión
@app.route('/indexEdi')
def indexEdi():
    if 'username' in session:
        # Obtener los edificios asociados al usuario
        username = session['username']
        edificios = get_edificios_por_usuario(username)
        return render_template('indexEdi.html', username=username, edificios=edificios)
    else:
        return redirect('/login')

# Función para obtener los edificios asociados a un usuario
def get_edificios_por_usuario(username):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT edificio_id, nombre, apartamentos, direccion, nit FROM Edificios WHERE usuario_id = ?", (username,))
    edificios = cursor.fetchall()
    print(edificios)
    conn.close()
    return edificios




# Obtener el nombre del edificio
def obtener_nombre_edificio(edificio_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM Edificios WHERE edificio_id = ?", (edificio_id,))
    nombre_edificio = cursor.fetchone()[0]
    conn.close()
    return nombre_edificio

# Función para obtener los datos de los bancos y la estructura de pago para RC del 1 al 5
def obtener_datos_edificio(edificio_id):
    # Conexión a la base de datos
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Consulta para obtener los datos de los bancos, la estructura de pago para RC del 1 al 5
    # y los nuevos campos
    cursor.execute('''
        SELECT Banco1, Cuenta1, tipo1, Banco2, Cuenta2, tipo2, Banco3, Cuenta3, tipo3, Banco4, Cuenta4, tipo4,
               estrucRC1, estrucRC2, estrucRC3, estrucRC4, estrucRC5, estrucRC6, estrucRC7,
               nombre, apartamentos, direccion, porteria, nit, porcentaje
        FROM Edificios
        WHERE edificio_id = ?
    ''', (edificio_id,))
    #0  1  2  3  4  5  6  7  8  9  10  11
    #12 13 14 15 16 17 18
    #19 20 21 22 23 24 25
    
    # Obtener los resultados de la consulta
    datos_edificio = cursor.fetchone()
    # Cerrar la conexión a la base de datos
    conn.close()
    
    # Retornar los datos obtenidos
    return datos_edificio

# Obtener bloques por edificio
def obtener_bloques(edificio_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT bloque FROM Propietarios WHERE edificio_id = ?", (edificio_id,))
    bloques = [row[0] for row in cursor.fetchall()]
    conn.close()
    return bloques

# Obtener propietarios por bloque
def obtener_propietarios_por_bloque(edificio_id, bloque):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, nombres, apellidos, apto, cedula, celular, direccion, parq, correo, CuotaADM, CuotaPARQ, CuotaEXT, Multa, Intereses, Retroactivos, CobroJuridico, fecha_emision, fecha_vencimiento, estado FROM Propietarios WHERE edificio_id = ? AND bloque = ?", (edificio_id, bloque))
    propietarios = cursor.fetchall()

    # Convertir el estado numérico a texto ("activo" o "desactivado")
    for i, propietario in enumerate(propietarios):
        estado_num = propietario[18]  # Último elemento de la tupla, que es el campo "estado"
        if estado_num == 1:
            propietarios[i] = propietario[:18] + ('activo',)  # Reemplazar el último elemento con "activo"
        elif estado_num == 0:
            propietarios[i] = propietario[:18] + ('desactivado',)  # Reemplazar el último elemento con "desactivado"

    conn.close()
    return propietarios


def insertar_propietario(edificio_id, apto, bloque, nombres, apellidos, cedula, celular, direccion, correo=None,
                         parq=None, cuotaADM=None, cuotaPARQ=None, cuotaEXT=None, multa=None, intereses=None,
                         fecha_emision=None, fecha_vencimiento=None, estado=None):
    # Obtener la fecha actual si no se proporciona fecha_emision
    if fecha_emision is None:
        fecha_emision = obtener_fecha_actual()

    # Calcular la fecha de vencimiento si no se proporciona fecha_vencimiento
    if fecha_vencimiento is None:
        # Suponiendo que la fecha de vencimiento es 30 días después de la fecha de emisión
        fecha_vencimiento = obtener_fecha_actual()

    # Realizar la conexión a la base de datos
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Insertar los datos del nuevo propietario en la base de datos
    cursor.execute('''
        INSERT INTO Propietarios (edificio_id, apto, bloque, nombres, apellidos, parq, cedula, celular, direccion,
                                  correo, cuotaADM, cuotaPARQ, cuotaEXT, multa, intereses, fecha_emision,
                                  fecha_vencimiento, estado) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (edificio_id, apto, bloque, nombres, apellidos, parq, cedula, celular, direccion, correo,
                    cuotaADM, cuotaPARQ, cuotaEXT, multa, intereses, fecha_emision, fecha_vencimiento, estado))
    
    # Guardar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

def obtener_cuentas_por_cobrar_fecha(edificio_id, estado, fecha_emision=None, user_id_ed=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    if fecha_emision and user_id_ed:
        cursor.execute("""
            SELECT CC.id_CXC, CC.user_id, CC.fecha_emision, CC.fecha_vencimiento, CC.estado AS estado_cuenta, P.nombres, P.apellidos, P.apto, P.bloque, P.correo,
                   CD.id AS detalle_id, CD.tipo, CD.monto, CD.pagado, CD.total, CD.descripcion
            FROM CuentasCobrar AS CC
            INNER JOIN Propietarios AS P ON CC.user_id = P.user_id
            LEFT JOIN CXCDetalle AS CD ON CC.id_CXC = CD.id_CXC
            WHERE CC.edificio_id = ? AND CC.fecha_emision = ? AND CC.user_id = ? AND CC.estado = ?
        """, (edificio_id, fecha_emision, user_id_ed, estado))
    elif fecha_emision:
        cursor.execute("""
            SELECT CC.id_CXC, CC.user_id, CC.fecha_emision, CC.fecha_vencimiento, CC.estado AS estado_cuenta, P.nombres, P.apellidos, P.apto, P.bloque, P.correo,
                   CD.id AS detalle_id, CD.tipo, CD.monto, CD.pagado, CD.total, CD.descripcion
            FROM CuentasCobrar AS CC
            INNER JOIN Propietarios AS P ON CC.user_id = P.user_id
            LEFT JOIN CXCDetalle AS CD ON CC.id_CXC = CD.id_CXC
            WHERE CC.edificio_id = ? AND CC.fecha_emision = ? AND CC.estado = ?
        """, (edificio_id, fecha_emision, estado))
    elif user_id_ed:
        cursor.execute("""
            SELECT CC.id_CXC, CC.user_id, CC.fecha_emision, CC.fecha_vencimiento, CC.estado AS estado_cuenta, P.nombres, P.apellidos, P.apto, P.bloque, P.correo,
                   CD.id AS detalle_id, CD.tipo, CD.monto, CD.pagado, CD.total, CD.descripcion
            FROM CuentasCobrar AS CC
            INNER JOIN Propietarios AS P ON CC.user_id = P.user_id
            LEFT JOIN CXCDetalle AS CD ON CC.id_CXC = CD.id_CXC
            WHERE CC.edificio_id = ? AND CC.user_id = ? AND CC.estado = ?
        """, (edificio_id, user_id_ed, estado))
    else:
        cursor.execute("""
            SELECT CC.id_CXC, CC.user_id, CC.fecha_emision, CC.fecha_vencimiento, CC.estado AS estado_cuenta, P.nombres, P.apellidos, P.apto, P.bloque, P.correo,
                   CD.id AS detalle_id, CD.tipo, CD.monto, CD.pagado, CD.total, CD.descripcion
            FROM CuentasCobrar AS CC
            INNER JOIN Propietarios AS P ON CC.user_id = P.user_id
            LEFT JOIN CXCDetalle AS CD ON CC.id_CXC = CD.id_CXC
            WHERE CC.edificio_id = ? AND CC.estado = ?
        """, (edificio_id, estado))
    
    cuentas = cursor.fetchall()
    
    cuentas_por_cobrar = {}
    for cuenta in cuentas:
        id_CXC, user_id, fecha_emision, fecha_vencimiento, estado_cuenta, nombres, apellidos, apto, bloque, correo, detalle_id, tipo, monto, pagado, total, descripcion = cuenta
        nombre_usuario = f"{nombres} {apellidos}"
        if id_CXC not in cuentas_por_cobrar:
            cuentas_por_cobrar[id_CXC] = {
                'id_CXC': id_CXC,
                'user_id': user_id,
                'usuario': nombre_usuario,
                'apto': apto,
                'bloque': bloque,
                'correo': correo,
                'fecha_emision': fecha_emision,
                'fecha_vencimiento': fecha_vencimiento,
                'estado': estado_cuenta,
                'detalles': []
            }
        if tipo is not None:  # Si hay detalles asociados
            cuentas_por_cobrar[id_CXC]['detalles'].append({
                'detalle_id': detalle_id,  # Asegúrate de incluir el ID del detalle
                'tipo': tipo,
                'monto': monto,
                'pagado': pagado,
                'total': total,
                'descripcion': descripcion
            })
    
    cuentas_por_cobrar_list = list(cuentas_por_cobrar.values())
    
    conn.close()
    return cuentas_por_cobrar_list


def obtener_recibos_caja_fecha(edificio_id, estado, fecha_emision=None, user_id_ed=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    if fecha_emision and user_id_ed:
        cursor.execute("""
            SELECT RC.id_RC, RC.user_id, RC.fecha, RC.descripcion, RC.tipopago, RC.valor, RC.estado AS estado_recibo,
                   RD.detalleID, RD.ID AS detalle_id, RD.cruceID, RD.id_CXC, RD.monto, RD.estado AS estado_detalle,
                   P.nombres, P.apellidos, P.apto, P.bloque, P.correo
            FROM ReciboCaja AS RC
            LEFT JOIN RCDetalles AS RD ON RC.id_RC = RD.id_RC
            LEFT JOIN Propietarios AS P ON RC.user_id = P.user_id
            WHERE RC.edificio_id = ? AND RC.fecha = ? AND RC.user_id = ? AND RC.estado = ?
        """, (edificio_id, fecha_emision, user_id_ed, estado))
    elif fecha_emision:
        cursor.execute("""
            SELECT RC.id_RC, RC.user_id, RC.fecha, RC.descripcion, RC.tipopago, RC.valor, RC.estado AS estado_recibo,
                   RD.detalleID, RD.ID AS detalle_id, RD.cruceID, RD.id_CXC, RD.monto, RD.estado AS estado_detalle,
                   P.nombres, P.apellidos, P.apto, P.bloque, P.correo
            FROM ReciboCaja AS RC
            LEFT JOIN RCDetalles AS RD ON RC.id_RC = RD.id_RC
            LEFT JOIN Propietarios AS P ON RC.user_id = P.user_id
            WHERE RC.edificio_id = ? AND RC.fecha = ? AND RC.estado = ?
        """, (edificio_id, fecha_emision, estado))
    elif user_id_ed:
        cursor.execute("""
            SELECT RC.id_RC, RC.user_id, RC.fecha, RC.descripcion, RC.tipopago, RC.valor, RC.estado AS estado_recibo,
                   RD.detalleID, RD.ID AS detalle_id, RD.cruceID, RD.id_CXC, RD.monto, RD.estado AS estado_detalle,
                   P.nombres, P.apellidos, P.apto, P.bloque, P.correo
            FROM ReciboCaja AS RC
            LEFT JOIN RCDetalles AS RD ON RC.id_RC = RD.id_RC
            LEFT JOIN Propietarios AS P ON RC.user_id = P.user_id
            WHERE RC.edificio_id = ? AND RC.user_id = ? AND RC.estado = ?
        """, (edificio_id, user_id_ed, estado))
    else:
        cursor.execute("""
            SELECT RC.id_RC, RC.user_id, RC.fecha, RC.descripcion, RC.tipopago, RC.valor, RC.estado AS estado_recibo,
                   RD.detalleID, RD.ID AS detalle_id, RD.cruceID, RD.id_CXC, RD.monto, RD.estado AS estado_detalle,
                   P.nombres, P.apellidos, P.apto, P.bloque, P.correo
            FROM ReciboCaja AS RC
            LEFT JOIN RCDetalles AS RD ON RC.id_RC = RD.id_RC
            LEFT JOIN Propietarios AS P ON RC.user_id = P.user_id
            WHERE RC.edificio_id = ? AND RC.estado = ?
        """, (edificio_id, estado))
    
    recibos = cursor.fetchall()
    
    recibos_caja = {}
    for recibo in recibos:
        id_RC, user_id, fecha, descripcion, tipopago, valor, estado_recibo, detalleID, detalle_id, cruceID, id_CXC, monto, estado_detalle, nombres, apellidos, apto, bloque, correo = recibo
        nombre_usuario = f"{nombres} {apellidos}"
        if id_RC not in recibos_caja:
            recibos_caja[id_RC] = {
                'id_RC': id_RC,
                'user_id': user_id,
                'fecha': fecha,
                'descripcion': descripcion,
                'tipopago': tipopago,
                'valor': valor,
                'estado_recibo': estado_recibo,
                'usuario': nombre_usuario,
                'apto': apto,
                'bloque': bloque,
                'correo': correo,
                'detalles': []
            }
        if detalle_id is not None:  # Si hay detalles asociados
            recibos_caja[id_RC]['detalles'].append({
                'detalle_id': detalle_id,
                'cruceID': cruceID,
                'detalleID': detalleID,  # Asegúrate de incluir el detalleID
                'id_CXC': id_CXC,
                'monto': monto,
                'estado_detalle': estado_detalle
            })
    
    recibos_caja_list = list(recibos_caja.values())
    
    conn.close()
    return recibos_caja_list





# ----------------------------------------------CXC----------------------------------------------



def obtener_ultimo_id_cxc(edificio_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id_CXC) FROM CuentasCobrar WHERE edificio_id = ?", (edificio_id,))
    resultado = cursor.fetchone()
    ultimo_id_cxc = resultado[0] if resultado[0] is not None else 0
    conn.close()  # Cierra la conexión después de obtener el ID
    return ultimo_id_cxc


def crear_cxc(id_CXC, user_id, edificio_id, fecha_emision, fecha_vencimiento, estado):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO CuentasCobrar (id_CXC, user_id, edificio_id, fecha_emision, fecha_vencimiento, estado)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_CXC, user_id, edificio_id, fecha_emision, fecha_vencimiento, estado))
    conn.commit()  # Confirma los cambios en la base de datos
    conn.close()  # Cierra la conexión después de crear la cuenta por cobrar

def agregar_detalle_cxc(id_CXC, user_id, tipo, monto, total, descripcion, estado, cuenta):
    pagado = 0.0
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO CXCDetalle (id_CXC, user_id, tipo, monto, pagado, total, descripcion, estado, cuenta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (id_CXC, user_id, tipo, monto, pagado, total, descripcion, estado, cuenta))
    conn.commit()  # Confirma los cambios en la base de datos
    conn.close()  # Cierra la conexión después de agregar el detalle a la cuenta por cobrar

def eliminar_cxc(id_CXC, user_id, edificio_id):
    """     print("edificio_id", edificio_id)
        print("id_CXC", id_CXC)
        print("user_id", user_id) """
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Eliminar entradas de CXCDetalle relacionadas con la cuenta por cobrar
        cursor.execute("DELETE FROM CXCDetalle WHERE id_CXC = ? AND user_id = ?", (id_CXC, user_id))

        # Eliminar la cuenta por cobrar especificada
        cursor.execute("DELETE FROM CuentasCobrar WHERE id_CXC = ? AND user_id = ? AND edificio_id = ?", (id_CXC, user_id, edificio_id))

        # Obtener el número de cuenta máximo posterior al ID eliminado
        cursor.execute("SELECT MAX(id_CXC) FROM CuentasCobrar WHERE id_CXC > ? AND user_id = ? AND edificio_id = ?", (id_CXC, user_id, edificio_id))
        max_id_posterior = cursor.fetchone()[0]

        # Si hay cuentas posteriores, actualizamos sus números de cuenta
        if max_id_posterior is not None:
            # Actualizar el número de cuenta de las cuentas posteriores
            cursor.execute("UPDATE CuentasCobrar SET id_CXC = id_CXC - 1 WHERE id_CXC > ? AND user_id = ? AND edificio_id = ?", (id_CXC, user_id, edificio_id))
            cursor.execute("UPDATE CXCDetalle SET id_CXC = id_CXC - 1 WHERE id_CXC > ? AND user_id = ?", (id_CXC, user_id))
        
        conn.commit()  # Confirmar los cambios en la base de datos
        conn.close()   # Cerrar la conexión
    except sqlite3.Error as e:
        print("Error al eliminar la CXC:", e, "numero edificio:", edificio_id)

def eliminar_detalle_cxc(detalle_id):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Eliminar el detalle específico de la tabla CXCDetalle
        cursor.execute("DELETE FROM CXCDetalle WHERE id = ?", (detalle_id,))

        conn.commit()  # Confirma los cambios en la base de datos
        conn.close()   # Cierra la conexión
    except sqlite3.Error as e:
        print("Error al eliminar el detalle de la CXC:", e)

def editar_detalle_cxc(detalle_id, descripcion, monto):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Actualizar la descripción y el monto del detalle específico en la tabla CXCDetalle
        cursor.execute("UPDATE CXCDetalle SET descripcion = ?, monto = ? WHERE id = ?", (descripcion, monto, detalle_id))

        conn.commit()  # Confirma los cambios en la base de datos
        conn.close()   # Cierra la conexión
    except sqlite3.Error as e:
        print("Error al editar el detalle de la CXC:", e)





# ----------------------------------------------RC----------------------------------------------
        

def buscar_ultimo_id_rc(edificio_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id_RC) FROM ReciboCaja WHERE edificio_id = ?", (edificio_id,))
    resultado = cursor.fetchone()
    ultimo_id_rc = resultado[0] if resultado[0] is not None else 0
    conn.close()
    return ultimo_id_rc

def crear_rc(id_RC, user_id, edificio_id, fecha, descripcion, tipopago, valor, estado):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ReciboCaja (id_RC, user_id, edificio_id, fecha, descripcion, tipopago, valor, estado) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (id_RC, user_id, edificio_id, fecha, descripcion, tipopago, valor, estado))
    conn.commit()
    conn.close()

def agregar_detalles_rc(id_RC, user_id, cruceID, detalleID, id_CXC, monto, estado):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO RCDetalles (id_RC, user_id, cruceID, detalleID, id_CXC, monto, estado) 
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (id_RC, user_id, cruceID, detalleID, id_CXC, monto, estado))
    conn.commit()
    conn.close()


def CXCDetalles_user_id(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM CXCDetalle WHERE user_id = ? AND cuenta = 1
    ''', (user_id,))
    detalles = cursor.fetchall()
    conn.close()
    column_names = [description[0] for description in cursor.description]
    detalles_con_nombres = [{column_names[i]: detalle[i] for i in range(len(column_names))} for detalle in detalles]
    return detalles_con_nombres
 

def realizar_pago(ID, pagado, total, pago_completo=True):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    if pago_completo:
        cursor.execute('''
            UPDATE CXCDetalle SET pagado = ?, total = ?, cuenta = 0 WHERE ID = ?
        ''', (pagado, total, ID))
    else:
        cursor.execute('''
            UPDATE CXCDetalle SET pagado = ?, total = ? WHERE ID = ?
        ''', (pagado, total, ID))
    conn.commit()
    conn.close()





# Ruta para la página de estadísticas
@app.route('/estadisticas/<int:edificio_id>/')
def estadisticas(edificio_id):
    # Verificar si el usuario ha iniciado sesión
    if 'username' in session:
        username = session['username']
    else:
        return redirect('/login')

    # Obtener el nombre del edificio
    nombre_edificio = obtener_nombre_edificio(edificio_id)

    # Verificar si se encontró el edificio
    if not nombre_edificio:
        # Si el edificio no existe, puedes manejar el error aquí o redirigir a una página de error
        return render_template('error.html', message="El edificio no existe")

    return render_template('estadisticas.html', edificio_id=edificio_id, nombre_edificio=nombre_edificio, username=username)

# Ruta para la página principal de propietarios
@app.route('/propietarios/<int:edificio_id>/')
def propietarios(edificio_id):
        
    if 'username' in session:  # Verificar si el usuario ha iniciado sesión
        username = session['username']  # Obtener el nombre de usuario de la sesión
    else:
        return redirect('/login')
    
    nombre_edificio = obtener_nombre_edificio(edificio_id)

    bloques = obtener_bloques(edificio_id)  # Agregar esta línea para obtener los bloques

    propietarios_por_bloque = {}
    for bloque in bloques:
        propietarios_por_bloque[bloque] = obtener_propietarios_por_bloque(edificio_id, bloque)

    # Pasar el documento plantilla a la plantilla HTML
    documento_plantilla = "plantilla.xlsx"

    return render_template('propietarios.html', edificio_id=edificio_id, nombre_edificio=nombre_edificio, 
                           username=username, bloques=bloques, propietarios_por_bloque=propietarios_por_bloque,
                           documento_plantilla=documento_plantilla)

# Ruta para la actualización de datos del propietario
@app.route('/actualizar_propietario', methods=['POST'])
def actualizar_propietario():
    if request.method == 'POST':
        # Obtener los datos del formulario
        user_id = request.form['user_id']  
        nombres = request.form['nombre']
        apellidos = request.form['apellido']
        bloque_id = request.form['bloque_id']
        cedula = request.form['cedula']
        celular = request.form['celular']
        direccion = request.form['direccion']
        parq = request.form['parq']
        correo = request.form['correo']

        # Realizar la actualización en la base de datos
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("UPDATE Propietarios SET nombres=?, apellidos=?, cedula=?, bloque=?, celular=?, direccion=?, parq=?, correo=? WHERE user_id=?", (nombres, apellidos, cedula, bloque_id, celular, direccion, parq, correo, user_id))

        # Confirmar y cerrar la conexión a la base de datos
        conn.commit()
        conn.close()

        return '', 204

@app.route('/accion', methods=['POST'])
def procesar_accion():
    edificio_id = request.form['edificio_id']
    user_id = request.form['user_id']  # Obtener el user_id del formulario
    accion = request.form['accion']
    
    # Aquí puedes realizar diferentes acciones dependiendo del botón presionado
    if accion == 'activar':
        # Código para activar al usuario específico
        cambiar_estado_propietario(user_id, True)
    elif accion == 'desactivar':
        # Código para desactivar al usuario específico
        cambiar_estado_propietario(user_id, False)
    elif accion == 'eliminar':
        # Código para eliminar al usuario específico
        eliminar_propietario(user_id)

    # Contar y actualizar propietarios en el edificio
    contar_y_actualizar_propietarios(edificio_id)
    
    return redirect(f'/propietarios/{edificio_id}/')

# Ruta para manejar la solicitud POST del formulario y agregar un nuevo propietario
@app.route('/agregar_propietario', methods=['POST'])
def agregar_propietario():
    if request.method == 'POST':
        # Obtener los datos del formulario
        edificio_id = request.form['edificio_id']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        apartamento_id = request.form['apartamento_id']
        bloque_id = request.form['bloque_id']
        cedula = request.form['cedula']
        celular = request.form['celular']
        direccion = request.form['direccion']
        parq = request.form['parq']
        correo = request.form['correo']
        estado = request.form['estado']  # Se puede omitir si no se necesita
        fecha_emision = obtener_fecha_actual()
        fecha_vencimiento = obtener_fecha_actual()

        # Contar y actualizar propietarios en el edificio
        contar_y_actualizar_propietarios(edificio_id)

        # Insertar los datos del nuevo propietario en la base de datos
        insertar_propietario(edificio_id, apartamento_id, bloque_id, nombre, apellido, cedula, celular, direccion,
                             correo, parq=parq, estado=estado, fecha_emision=fecha_emision,
                             fecha_vencimiento=fecha_vencimiento)

        return redirect(f'/propietarios/{edificio_id}/')

@app.route('/agregar_propietarios', methods=['POST'])
def agregar_propietarios():
    if 'username' not in session:  # Verificar si el usuario ha iniciado sesión
        return redirect('/login')

    documento_pago = request.files['documento_pago']

    # Leer el archivo Excel
    df = pd.read_excel(documento_pago)

    edificio_id = request.form.get('edificio_id')
    # Asignar el valor predefinido para edificio_id
    df['edificio_id'] = edificio_id

    estado = 1
    df['estado'] = estado

    # Asignar la fecha actual para fecha_emision y fecha_vencimiento
    fecha_actual = datetime.today().strftime("%Y-%m-%d")
    df['fecha_emision'] = fecha_actual
    df['fecha_vencimiento'] = fecha_actual

    # Insertar los datos en la base de datos
    insertar_datos_desde_dataframe(df)

    # Contar y actualizar propietarios en el edificio
    contar_y_actualizar_propietarios(edificio_id)

    return redirect('/propietarios/{}'.format(edificio_id))


# Función para insertar datos desde un DataFrame en la base de datos
def insertar_datos_desde_dataframe(df):
    conn = sqlite3.connect(DATABASE)
    df.to_sql('Propietarios', conn, if_exists='append', index=False)
    conn.close()

# Función para cambiar el estado del propietario
def cambiar_estado_propietario(user_id, nuevo_estado):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE Propietarios SET estado = ? WHERE user_id = ?", (nuevo_estado, user_id))
    conn.commit()
    conn.close()

# Función para eliminar un propietario
def eliminar_propietario(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Propietarios WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def contar_y_actualizar_propietarios(edificio_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Contar los propietarios en el edificio
    cursor.execute("SELECT COUNT(*) FROM Propietarios WHERE edificio_id = ?", (edificio_id,))
    count = cursor.fetchone()[0]

    # Actualizar la tabla de edificios con el recuento de propietarios
    cursor.execute("UPDATE Edificios SET apartamentos = ? WHERE edificio_id = ?", (count, edificio_id))

    conn.commit()
    conn.close()

@app.route('/cobros/<int:edificio_id>/')
def cobros(edificio_id):

    if 'username' in session:  # Verificar si el usuario ha iniciado sesión
        username = session['username']  # Obtener el nombre de usuario de la sesión
    else:
        return redirect('/login')
    
    user_id = session.get('user_id')  # Obtener el user_id del usuario logueado
    
    nombre_edificio = obtener_nombre_edificio(edificio_id)
    bloques = obtener_bloques(edificio_id)  # Agregar esta línea para obtener los bloques
    
    propietarios_por_bloque = {}
    for bloque in bloques:
        propietarios_por_bloque[bloque] = obtener_propietarios_por_bloque(edificio_id, bloque)
    
    return render_template('cobros.html', edificio_id=edificio_id, user_id=user_id, nombre_edificio=nombre_edificio,
                           username=username, bloques=bloques, propietarios_por_bloque=propietarios_por_bloque,
                           )


# Ruta para la actualización de datos del propietario
@app.route('/actualizar_cobros', methods=['POST'])
def actualizar_cobros_propietario():  
    if request.method == 'POST':
        edificio_id = request.form['modal_edificio_id']
        # Obtener los datos del formulario
        user_id = request.form['user_id']  
        cuotaADM = request.form['cuotaADM']  # Campo "Admin"
        cuotaPARQ = request.form['cuotaPARQ']  # Campo "Parq"
        cuotaEXT = request.form['cuotaEXT']  # Campo "Cuota Extra"
        multa = request.form['multa']  # Campo "Multa"
        intereses = request.form['intereses']  # Campo "Intereses"
        retroactivos = request.form['retroactivos']  # Campo "Retroactivos"
        cobroJuridico = request.form['cobroJuridico']  # Campo "CobroJuridico"
        fecha_emision = request.form['fecha_emision']  # Campo "fecha_emision"
        fecha_vencimiento = request.form['fecha_vencimiento']  # Campo "fecha_vencimiento"

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("UPDATE Propietarios SET CuotaADM=?, CuotaPARQ=?, CuotaEXT=?, Multa=?, Intereses=?, Retroactivos=?, CobroJuridico=?, fecha_emision=?, fecha_vencimiento=? WHERE user_id=?", (cuotaADM, cuotaPARQ, cuotaEXT, multa, intereses, retroactivos, cobroJuridico, fecha_emision, fecha_vencimiento, user_id))

        # Confirmar y cerrar la conexión a la base de datos
        conn.commit()
        conn.close()

        return redirect(f'/cobros/{edificio_id}/')


# Ruta para actualizar las fechas de emisión y vencimiento de todos los propietarios de un edificio
@app.route('/fechas_plantilla', methods=['POST'])
def fechas_plantilla():
    if request.method == 'POST':
        # Obtener las fechas de emisión y vencimiento del formulario
        edificio_id = request.form['edificio_id']
        fecha_emision = request.form['fecha_emision']
        fecha_vencimiento = request.form['fecha_vencimiento']

        # Conectar a la base de datos
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Actualizar las fechas de emisión y vencimiento de los propietarios del edificio
        cursor.execute("UPDATE Propietarios SET fecha_emision=?, fecha_vencimiento=? WHERE edificio_id=?", (fecha_emision, fecha_vencimiento, edificio_id))

        # Confirmar y cerrar la conexión a la base de datos
        conn.commit()
        conn.close()

        # Redireccionar a la página de pagos del edificio actualizado
        return redirect(f'/cobros/{edificio_id}/')


# Ruta crear cxc manual
@app.route('/crear_cxc_manual', methods=['POST'])
def crear_cxc_manual():
    if request.method == 'POST':
        
        edificio_id = request.form['edificio_id']
        user_id = request.form['user_id']

        # Obtener el último id_CXC del edificio
        ultimo_id_cxc = obtener_ultimo_id_cxc(edificio_id)
        id_CXC = ultimo_id_cxc + 1  # Incrementar el id_CXC

        # Conectar a la base de datos
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Obtener los detalles de la cuenta por cobrar para el usuario específico
        cursor.execute("SELECT CuotaADM, CuotaPARQ, CuotaEXT, Multa, Intereses, Retroactivos, CobroJuridico, fecha_emision, fecha_vencimiento FROM Propietarios WHERE edificio_id = ? AND user_id = ? ", (edificio_id, user_id))
        cuenta_cxc = cursor.fetchone()

        # Confirmar y cerrar la conexión a la base de datos
        conn.commit()
        conn.close()

        if cuenta_cxc:  # Si se encontraron detalles de la cuenta por cobrar
            cuotaADM, cuotaPARQ, cuotaEXT, multa, intereses, retroactivos, cobro_juridico, fecha_emision, fecha_vencimiento = cuenta_cxc
            
            # Crear la cuenta de cobro
            crear_cxc(id_CXC, user_id, edificio_id, fecha_emision, fecha_vencimiento, "Pendiente")
            
            # Agregar detalles a la cuenta de cobro
            if cuotaADM is not None and cuotaADM != 0:
                agregar_detalle_cxc(id_CXC, user_id, "Administracion", cuotaADM, cuotaADM, "Cuota de Administración", "Pendiente", True)
            if cuotaPARQ is not None and cuotaPARQ != 0:
                agregar_detalle_cxc(id_CXC, user_id, "Parqueaderos", cuotaPARQ, cuotaPARQ, "Cuota de Parqueadero", "Pendiente", True)
            if cuotaEXT is not None and cuotaEXT != 0:
                agregar_detalle_cxc(id_CXC, user_id, "Extra", cuotaEXT, cuotaEXT, "Cuota Extra Fija", "Pendiente", True)
            if multa is not None and multa != 0:
                agregar_detalle_cxc(id_CXC, user_id, "Multa", multa, multa, "Multa Administrativa por inasistencia", "Pendiente", True)
            if intereses is not None and intereses != 0:
                agregar_detalle_cxc(id_CXC, user_id, "Intereses", intereses, intereses, "Intereses", "Pendiente", True)
            if retroactivos is not None and retroactivos != 0:
                agregar_detalle_cxc(id_CXC, user_id, "Retroactivos", retroactivos, retroactivos, "Retroactivos", "Pendiente", True)
            if cobro_juridico is not None and cobro_juridico != 0:
                agregar_detalle_cxc(id_CXC, user_id, "CobroJuridico", cobro_juridico, cobro_juridico, "Cobro Jurídico", "Pendiente", True)

            print("Cuenta por cobrar creada manualmente para el usuario ID:", user_id)
        else:
            print("No se encontraron detalles de la cuenta por cobrar para el usuario ID:", user_id)
        
        # Redireccionar a la página de cobros del edificio actualizado
        return redirect(f'/cobros/{edificio_id}/')




# Ruta para la contabilización automática
@app.route('/contabilizar_automatico/', methods=['POST'])
def contabilizar_automatico():
    edificio_id = request.form.get('edificio_id_CXCautomatico')
    # Obtener el último id_CXC del edificio
    ultimo_id_cxc = obtener_ultimo_id_cxc(edificio_id)
    # Conectar a la base de datos
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Crear cuentas de cobro para cada propietario
    cursor.execute("SELECT user_id, CuotaADM, CuotaPARQ, CuotaEXT, Multa, Intereses, Retroactivos, CobroJuridico, fecha_emision, fecha_vencimiento FROM Propietarios WHERE edificio_id = ? AND estado = ?", (edificio_id, 1))
    propietarios = cursor.fetchall()

    # Confirmar y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

    for propietario in propietarios:
        user_id, cuotaADM, cuotaPARQ, cuotaEXT, multa, intereses, retroactivos, cobro_juridico, fecha_emision, fecha_vencimiento = propietario
            
        # Verificar que ninguno de los campos sea None
        if (cuotaADM, cuotaPARQ, cuotaEXT, multa, intereses, retroactivos, cobro_juridico):
            ultimo_id_cxc += 1  # Incrementar el id_CXC
            id_CXC = ultimo_id_cxc
            
            # Crear la cuenta de cobro
            crear_cxc(id_CXC, user_id, edificio_id, fecha_emision, fecha_vencimiento, "Pendiente")
            
            # Agregar detalles a la cuenta de cobro
            if cuotaADM is not None and cuotaADM != 0:
                agregar_detalle_cxc(id_CXC, user_id, "Administracion", cuotaADM, cuotaADM, "Cuota de Administración", "Pendiente", True)
            if cuotaPARQ is not None and cuotaPARQ != 0:
                agregar_detalle_cxc(id_CXC, user_id, "Parqueaderos", cuotaPARQ, cuotaPARQ, "Cuota de Parqueadero", "Pendiente", True)
            if cuotaEXT is not None and cuotaEXT != 0:
                agregar_detalle_cxc(id_CXC, user_id, "Extra", cuotaEXT, cuotaEXT, "Cuota Extra Fija", "Pendiente", True)
            if multa is not None and multa != 0:
                agregar_detalle_cxc(id_CXC, user_id, "Multa", multa, multa, "Multa Administrativa por inasistencia", "Pendiente", True)
            if intereses is not None and intereses != 0:
                agregar_detalle_cxc(id_CXC, user_id, "Intereses", intereses, intereses, "Intereses", "Pendiente", True)
            if retroactivos is not None and retroactivos != 0:
                agregar_detalle_cxc(id_CXC, user_id, "Retroactivos", retroactivos, retroactivos, "Retroactivos", "Pendiente", True)
            if cobro_juridico is not None and cobro_juridico != 0:
                agregar_detalle_cxc(id_CXC, user_id, "CobroJuridico", cobro_juridico, cobro_juridico, "Cobro Jurídico", "Pendiente", True)

            # Actualizar intereses del propietario a 0
            actualizar_intereses_propietario(user_id, 0)

            print("Contabilización automática realizada para el edificio ID:", edificio_id)
        else:
            print("No se encontraron detalles para la Contabilización automática edificio ID:", edificio_id)


    
    # Puedes redireccionar a alguna página después de realizar la contabilización automática
    return redirect(f'/cobros/{edificio_id}/')


@app.route('/pagos/<int:edificio_id>/')
def pagos(edificio_id):

    if 'username' in session:  # Verificar si el usuario ha iniciado sesión
        username = session['username']  # Obtener el nombre de usuario de la sesión
    else:
        return redirect('/login')
    
    user_id = session.get('user_id')  # Obtener el user_id del usuario logueado
    
    nombre_edificio = obtener_nombre_edificio(edificio_id)
    bloques = obtener_bloques(edificio_id)  # Agregar esta línea para obtener los bloques
    
    propietarios_por_bloque = {}
    for bloque in bloques:
        propietarios_por_bloque[bloque] = obtener_propietarios_por_bloque(edificio_id, bloque)
    
    # Obtener los datos de los bancos y la estructura de pago para RC del 1 al 5
    datos_edificio = obtener_datos_edificio(edificio_id)
    bancos = datos_edificio[0],datos_edificio[3],datos_edificio[6],datos_edificio[9]
    estructura_rc = datos_edificio[12:19]
    
    return render_template('pagos.html', edificio_id=edificio_id, user_id=user_id, nombre_edificio=nombre_edificio,
                           username=username, bloques=bloques, propietarios_por_bloque=propietarios_por_bloque,
                           bancos=bancos, estructura_rc=estructura_rc)

# Ruta para manejar la creación de un pago
@app.route('/crear_pago', methods=['POST'])
def crear_pago():
    if request.method == 'POST':
        # Obtener los datos del formulario
        edificio_id = request.form['edificio_id']
        user_id = request.form['user_id']
        fecha = request.form['fecha']
        descripcion = request.form['descripcion']
        tipopago = request.form['tipopago']
        valor = int(request.form['valor'])
        estado = request.form['estado']

    detalles = CXCDetalles_user_id(user_id)
    datos_edificio = obtener_datos_edificio(edificio_id)
    estrucRC1, estrucRC2, estrucRC3, estrucRC4, estrucRC5, estrucRC6, estrucRC7 = datos_edificio[12:19]
    estructuras_pago = [estrucRC1, estrucRC2, estrucRC3, estrucRC4, estrucRC5, estrucRC6, estrucRC7]
    
    saldo_disponible = valor
    
    # Organizar los detalles de CXC según los tipos de orden de la estructura
    detalles_organizados = {
        estrucRC1: [],
        estrucRC2: [],
        estrucRC3: [],
        estrucRC4: [],
        estrucRC5: [],
        estrucRC6: [],
        estrucRC7: []
    }

    for detalle in detalles:
        tipo = detalle['tipo']
        if tipo == estrucRC1:
            detalles_organizados[estrucRC1].append(detalle)
        elif tipo == estrucRC2:
            detalles_organizados[estrucRC2].append(detalle)
        elif tipo == estrucRC3:
            detalles_organizados[estrucRC3].append(detalle)
        elif tipo == estrucRC4:
            detalles_organizados[estrucRC4].append(detalle)
        elif tipo == estrucRC5:
            detalles_organizados[estrucRC5].append(detalle)
        elif tipo == estrucRC6:
            detalles_organizados[estrucRC6].append(detalle)
        elif tipo == estrucRC7:
            detalles_organizados[estrucRC7].append(detalle)
    
    # Ordenar los detalles de cada estructura por id_CXC de menor a mayor
    for estructura in estructuras_pago:
        detalles_estructura = sorted(detalles_organizados.get(estructura, []), key=lambda x: x['id_CXC'])
        detalles_organizados[estructura] = detalles_estructura

    # Realizar el pago de las cuentas
    id_RC = buscar_ultimo_id_rc(edificio_id) + 1
    crear_rc(id_RC, user_id, edificio_id, fecha, descripcion, tipopago, valor, estado)

    for estructura in estructuras_pago:
        detalles_estructura = detalles_organizados.get(estructura, [])
        for detalle in detalles_estructura:
            if saldo_disponible > 0:  # Mientras haya saldo disponible
                monto_a_pagar = detalle['monto'] - detalle['pagado']  # Calcular el monto que falta por pagar
                if monto_a_pagar > 0:  # Si hay algo para pagar
                    monto_a_pagar = min(saldo_disponible, monto_a_pagar)  # Pagar con saldo disponible o el monto faltante, lo que sea menor
                    if detalle['pagado'] + monto_a_pagar == detalle['monto']:  # Verificar si el pago es completo
                        realizar_pago(detalle['ID'], detalle['pagado'] + monto_a_pagar, 0, pago_completo=True)
                    else:
                        realizar_pago(detalle['ID'], detalle['pagado'] + monto_a_pagar, detalle['monto'] - (detalle['pagado'] + monto_a_pagar), pago_completo=False)
                    saldo_disponible -= monto_a_pagar  # Actualizar saldo disponible
                    print(f"Se ha pagado {monto_a_pagar} para {detalle['descripcion']}")
                    agregar_detalles_rc(id_RC, user_id, detalle['ID'], detalle['descripcion'], detalle['id_CXC'], monto_a_pagar, estado)
            else:
                print("No hay saldo disponible para pagar más facturas.")
                break
            
    # Verificar si queda saldo a favor
    if saldo_disponible > 0:
        estado = "SaldoFavor"
        detalleID = "Saldo a Favor"
        agregar_detalles_rc(id_RC, user_id, 0, detalleID, 0, saldo_disponible, estado)
        print("Saldo a favor:", saldo_disponible, estado )

    return redirect(f'/pagos/{edificio_id}/')


# Ruta para manejar la creación de una cuenta de cobro manual
@app.route('/crear_rc_manual', methods=['POST'])
def crear_rc_manual():
    if request.method == 'POST':
        # Obtener los datos del formulario
        user_id = request.form['user_id']
        edificio_id = request.form['edificio_id']

        # Aquí puedes agregar la lógica para crear la cuenta de cobro manual en la base de datos o realizar cualquier otro procesamiento necesario
        
        # En este ejemplo, simplemente mostraremos los datos recibidos
        return f"Cuenta de cobro manual creada: user_id={user_id}, edificio_id={edificio_id}"


# Ruta para manejar la solicitud POST y contabilizar
@app.route('/cambio_estado', methods=['POST'])
def contabilizar():
    if request.method == 'POST':
        # Obtener los datos del formulario
        cuenta = request.form['cuenta']
        id_cuenta = request.form['id_cuenta']
        user_id = request.form['user_id']
        estado = request.form['estado']
        edificio_id = request.form['edificio_id']
        pagina = request.form['pagina']

        # Verificar el tipo de cuenta y llamar a la función correspondiente
        if cuenta == 'CXC':
            contabilizar_cxc(id_cuenta, user_id, estado)
        elif cuenta == 'RC':
            contabilizar_rc(id_cuenta, user_id, estado)

        # Redirigir a una página de éxito o a donde desees
        return redirect(f'/{pagina}/{edificio_id}/')

    
def contabilizar_cxc(id_CXC, user_id, edificio_id, estado):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Actualizar el estado en la tabla CuentasCobrar
    cursor.execute('''
        UPDATE CuentasCobrar
        SET estado = ?
        WHERE id_CXC = ? AND user_id = ? AND edificio_id = ?
    ''', (estado, id_CXC, user_id, edificio_id))

    # Actualizar el estado en la tabla CXCDetalle
    cursor.execute('''
        UPDATE CXCDetalle
        SET estado = ?
        WHERE id_CXC = ? AND user_id = ?
    ''', (estado, id_CXC, user_id))



    #create_pdf_CXC(id_CXC, user_id, edificio_id)

    print(id_CXC)

    conn.commit()
    conn.close()

def contabilizar_rc(id_cuenta, user_id, estado):
    print(id_cuenta,user_id,estado)


@app.route('/contabilizar_lista_cxc', methods=['POST'])
def contabilizar_lista_cxc():
    edificio_id = request.form['edificio_id']  # Obtener edificio_id
    if request.form['accion'] == 'contabilizar':
        # Obtener la lista de cuentas por cobrar desde el formulario
        lista_cxc = request.form.getlist('lista_cxc')
        estado = 'Contabilizado'

        # Contabilizar las cuentas por cobrar de la lista
        for cxc in lista_cxc:
            id_CXC, user_id = map(int, cxc.split('-'))
            contabilizar_cxc(id_CXC, user_id, edificio_id, estado)
            # Llamar a la función para crear el PDF
            create_pdf_with_reportlab("CXC.pdf", id_CXC, user_id, edificio_id)

        # Redirigir a una página de éxito o a donde desees
        return redirect(f'/pendiente/{edificio_id}/')
    
    elif request.form['accion'] == 'enviar':
        # Obtener la lista de cuentas por cobrar desde el formulario
        lista_cxc = request.form.getlist('lista_cxc')
        estado = 'Contabilizado'

        # Contabilizar las cuentas por cobrar de la lista
        for cxc in lista_cxc:
            id_CXC, user_id = map(int, cxc.split('-'))
            contabilizar_cxc(id_CXC, user_id, edificio_id, estado)

        # Redirigir a una página de éxito o a donde desees
        return redirect(f'/pendiente/{edificio_id}/')
    
    elif request.form['accion'] == 'descargar':
        # Obtener la lista de cuentas por cobrar desde el formulario
        lista_cxc = request.form.getlist('lista_cxc')
        estado = 'Contabilizado'

        # Contabilizar las cuentas por cobrar de la lista
        for cxc in lista_cxc:
            id_CXC, user_id = map(int, cxc.split('-'))
            contabilizar_cxc(id_CXC, user_id, edificio_id, estado)

        # Redirigir a una página de éxito o a donde desees
        return redirect(f'/pendiente/{edificio_id}/')

    elif request.form['accion'] == 'eliminar':
        # Obtener la lista de cuentas por cobrar desde el formulario
        lista_cxc = request.form.getlist('lista_cxc')

        # Eliminar todas las cuentas por cobrar de la lista
        for cxc in lista_cxc:
            id_CXC, user_id = map(int, cxc.split('-'))
            eliminar_cxc(id_CXC, user_id, edificio_id)

        # Redirigir a una página de éxito o a donde desees
        return redirect(f'/pendiente/{edificio_id}/')

#def create_pdf_CXC(id_CXC, user_id, edificio_id):

@app.route('/crear_deuda', methods=['POST'])
def crear_multa():
    id_CXC = request.form['id_CXC']  # Obtener la ID_CXC del formulario
    user_id = request.form['user_id']  
    tipo = request.form['tipo']  # Obtener el tipo de multa del formulario
    monto = request.form['monto']
    descripcion = request.form['descripcion']
    estado = 'pendiente'  # Valor predeterminado
    cuenta = True
    edificio_id = request.form['edificio_id']  # Obtener edificio_id
    
    agregar_detalle_cxc(id_CXC, user_id, tipo, monto, monto, descripcion, estado, cuenta)  # El total se establece en 0

    return redirect(f'/pendiente/{edificio_id}/')

@app.route('/eliminar_cxc', methods=['POST'])
def eliminar_cxc_route():
    id_CXC = request.form['id_CXC']  # Obtener la ID_CXC del formulario
    user_id = request.form['user_id']  
    edificio_id = request.form['edificio_id']  # Obtener edificio_id

    eliminar_cxc(id_CXC, user_id, edificio_id)

    return redirect(f'/pendiente/{edificio_id}/')

@app.route('/eliminar_detalle_cxc', methods=['POST'])
def eliminar_detalle_cxc_route():
    detalle_id = request.form['detalle_id']  # Obtener el ID del detalle del formulario
    edificio_id = request.form['edificio_id']  # Obtener edificio_id

    eliminar_detalle_cxc(detalle_id)  # Llama a la función eliminar_detalle_cxc con el detalle_id
    #print("Eliminando detalle ID", detalle_id)
    
    return redirect(f'/pendiente/{edificio_id}/')

@app.route('/editar_detalle_cxc', methods=['POST'])
def editar_detalle_cxc_route():
    detalle_id = request.form['detalle_id']  # Obtener el ID del detalle del formulario
    descripcion = request.form['descripcion']  # Obtener la nueva descripción del formulario
    monto = request.form['monto']  # Obtener el nuevo monto del formulario
    edificio_id = request.form['edificio_id']  # Obtener el ID del edificio del formulario
    
    editar_detalle_cxc(detalle_id, descripcion, monto)  # Llama a la función para editar el detalle
    #print("Editando detalle", detalle_id)
    
    return redirect(f'/pendiente/{edificio_id}/')


# Ruta para la página de contabilidad
@app.route('/pendiente/<int:edificio_id>/')
def pendiente(edificio_id):
    if 'username' in session:  # Verificar si el usuario ha iniciado sesión
        username = session['username']  # Obtener el nombre de usuario de la sesión
    else:
        return redirect('/login')
    
    nombre_edificio = obtener_nombre_edificio(edificio_id)

    estado = request.args.get('estado') # Obtener el estado de la cxc
    user_id_ed = request.args.get('user_id') # Obtener el user_id
    fecha_emision = request.args.get('fecha_emision')  # Obtener la fecha de emisión filtrada
    
    cuentas_por_cobrar = []

    if fecha_emision is None:  # Si no se proporciona fecha_emision, establecer la fecha del día
        fecha_emision = obtener_fecha_actual()
        estado = "Pendiente"
        
    if fecha_emision:
        cuentas_por_cobrar = obtener_cuentas_por_cobrar_fecha(edificio_id, estado, fecha_emision=fecha_emision, user_id_ed=user_id_ed)
    else:
        cuentas_por_cobrar = obtener_cuentas_por_cobrar_fecha(edificio_id, estado, user_id_ed=user_id_ed)

    return render_template('pendiente.html', edificio_id=edificio_id, nombre_edificio=nombre_edificio, username=username, cuentas_por_cobrar=cuentas_por_cobrar)

# Ruta para la página de contabilidad
@app.route('/contabilizado/<int:edificio_id>/')
def contabilizado(edificio_id):
    if 'username' in session:  # Verificar si el usuario ha iniciado sesión
        username = session['username']  # Obtener el nombre de usuario de la sesión
    else:
        return redirect('/login')
    
    nombre_edificio = obtener_nombre_edificio(edificio_id)

    estado = request.args.get('estado') # Obtener el estado de la cxc
    user_id_ed = request.args.get('user_id') # Obtener el user_id
    fecha_emision = request.args.get('fecha_emision')  # Obtener la fecha de emisión filtrada

    tipo_cuenta = request.args.get('tipo_cuenta') # Obtener el tipo de cuenta
    
    cuentas_por_cobrar = []
    
    resivos_caja = []

    if tipo_cuenta == 'CXC_AMD':
        if fecha_emision:
            cuentas_por_cobrar = obtener_cuentas_por_cobrar_fecha(edificio_id, estado, fecha_emision=fecha_emision, user_id_ed=user_id_ed)
        else:
            cuentas_por_cobrar = obtener_cuentas_por_cobrar_fecha(edificio_id, estado, user_id_ed=user_id_ed)
    elif tipo_cuenta == 'RC_AMD':
        if fecha_emision:
            resivos_caja = obtener_recibos_caja_fecha(edificio_id, estado, fecha_emision=fecha_emision, user_id_ed=user_id_ed)
        else:
            resivos_caja = obtener_recibos_caja_fecha(edificio_id, estado, user_id_ed=user_id_ed)
    else:
        # Tipo de cuenta no reconocido
        # Puedes manejar este caso como desees, por ejemplo, lanzar un error o redirigir a una página de error
        pass

    return render_template('contabilizado.html', edificio_id=edificio_id, nombre_edificio=nombre_edificio, username=username, cuentas_por_cobrar=cuentas_por_cobrar, recibos_caja=resivos_caja)



@app.route('/calcular_intereses', methods=['POST'])
def calcular_intereses():
    edificio_id = request.form.get('edificio_id_intereses_extra')

    # Obtener el porcentaje de intereses asociado al edificio
    porcentaje_intereses = obtener_porcentaje_intereses(edificio_id)

    # Obtener todos los user_ids asociados al edificio
    user_ids = obtener_user_ids_por_edificio(edificio_id)

    # Calcular y actualizar los intereses adicionales para cada user_id
    for user_id in user_ids:
        total_deuda = obtener_deuda_por_user_id(user_id)
        #print(total_deuda)
        intereses_adicionales = (total_deuda * porcentaje_intereses) / 100 if porcentaje_intereses else 0
        
        # Redondear a 2 decimales
        intereses_adicionales_rounded = round(intereses_adicionales, 2)

        actualizar_intereses_propietario(user_id, intereses_adicionales_rounded)
    return redirect(f'/cobros/{edificio_id}/')

def obtener_porcentaje_intereses(edificio_id):
    # Conexión a la base de datos
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Consulta para obtener el porcentaje de intereses del edificio
    cursor.execute('''
        SELECT porcentaje FROM Edificios WHERE edificio_id = ?
    ''', (edificio_id,))
    
    # Obtener el porcentaje de intereses
    porcentaje = cursor.fetchone()

    # Cerrar la conexión y retornar el porcentaje
    conn.close()
    return porcentaje[0] if porcentaje else None

def obtener_user_ids_por_edificio(edificio_id):
    # Conexión a la base de datos
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Consulta para obtener todos los user_ids asociados al edificio
    cursor.execute('''
        SELECT user_id FROM Propietarios WHERE edificio_id = ?
    ''', (edificio_id,))
    
    # Obtener los user_ids
    user_ids = [row[0] for row in cursor.fetchall()]

    # Cerrar la conexión y retornar los user_ids
    conn.close()
    return user_ids

def obtener_deuda_por_user_id(user_id):
    # Conexión a la base de datos
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Consulta para obtener la suma de la deuda del user_id, excluyendo CobroJuridico e Intereses
    cursor.execute('''
        SELECT SUM(total) FROM CXCDetalle 
        WHERE user_id = ? 
        AND estado = 'Contabilizado' 
        AND cuenta = 1 
        AND tipo NOT IN ('CobroJuridico', 'Intereses')
    ''', (user_id,))
    
    # Obtener la suma de la deuda
    total_deuda = cursor.fetchone()[0] or 0

    # Cerrar la conexión y retornar la suma de la deuda
    conn.close()
    return total_deuda



def actualizar_intereses_propietario(user_id, intereses_adicionales):
    # Conexión a la base de datos
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Actualizar los intereses adicionales para el user_id
    cursor.execute('''
        UPDATE Propietarios
        SET Intereses = ?
        WHERE user_id = ?
    ''', (intereses_adicionales, user_id))

    # Confirmar la transacción y cerrar la conexión
    conn.commit()
    conn.close()


# Ruta para la página de informes
@app.route('/informes/<int:edificio_id>/')
def informes(edificio_id):
    if 'username' in session:# Verificar si el usuario ha iniciado sesión
        username = session['username']# Obtener el nombre de usuario de la sesión
    else:
        return redirect('/login')
    
    nombre_edificio = obtener_nombre_edificio(edificio_id)
    

    return render_template('informes.html', edificio_id=edificio_id, nombre_edificio=nombre_edificio, username=username)

@app.route('/configuracion/<int:edificio_id>/')
def configuracion(edificio_id):
    if 'username' in session:  # Verificar si el usuario ha iniciado sesión
        username = session['username']  # Obtener el nombre de usuario de la sesión
    else:
        return redirect('/login')
    
    datos_edificio = obtener_datos_edificio(edificio_id)
    
    return render_template('configuracion.html', edificio_id=edificio_id, username=username, datos_edificio=datos_edificio)








@app.route('/activar_riego')
def activar_riego():
    # Lógica para activar el riego (puedes llamar a una función específica aquí)
    # ...

    return 'Riego 10 minutos'

@app.route('/activar_ventilacion')
def activar_ventilacion():
    # Lógica para activar la ventilación (puedes llamar a una función específica aquí)
    # ...

    return 'Ventilación 10 minutos'

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))



#-------------------------------------      pdf    ------------------------------------------------

# Función para crear el PDF utilizando ReportLab
def create_pdf_with_reportlab(filename, id_CXC, user_id, edificio_id):
    # Obtener los datos para el PDF
    datos_factura = create_pdf_CXC(id_CXC, user_id, edificio_id)
    
    # Crear el documento PDF
    c = canvas.Canvas(filename, pagesize=letter)

    # Agregar imagen de fondo
    background_image = "domyclip-adm/static/CXC simple azul.jpg"  # Ruta de la imagen de fondo
    c.drawImage(background_image, 0, 0, width=letter[0], height=letter[1])

    # Agregar icono en la parte superior derecha
    icon_image = "domyclip-adm/static/bg.jpg"  # Ruta de la imagen del icono
    c.drawImage(icon_image, 50, letter[1] - 140, width=100, height=100)

    # Establecer color y tipografía del texto
    c.setFillColorRGB(0.17, 0.27, 0.74)  # Color negro
    c.setFont("PoppinsBold", 20)  # Tipografía Helvetica, tamaño de fuente 12

    # Agregar detalles del edificio
    c.drawString(180, 722, datos_factura['nombre_edificio'])
    c.drawString(180, 692, "NIT: " + datos_factura['nit'])

    c.setFillColorRGB(0, 0, 0)  # Color negro
    c.setFont("PoppinsRegular", 12)  # Tipografía Helvetica, tamaño de fuente 12

    # Agregar información del propietario
    c.drawString(75, 552, datos_factura['nombres_propietario'])
    c.drawString(75, 539, "CC: " + datos_factura['cedula_propietario'])
    c.drawString(75, 526, "Cel: " + datos_factura['celular_propietario'])
    c.drawString(75, 513, "Dir: " + datos_factura['direccion_propietario'])
    c.drawString(75, 500, "Correo: " + datos_factura['correo_propietario'])

    # Agregar información del administrador
    c.drawString(340, 552, datos_factura['nombre_amd_edificio'])
    c.drawString(340, 539, "CC: " + datos_factura['cedula_amd_edificio'])
    c.drawString(340, 526, "Cel: " + datos_factura['celular_amd_edificio'])
    c.drawString(340, 513, "Fecha: " + datos_factura['fecha_emision'])
    c.drawString(340, 500, "Correo: " + datos_factura['correo_amd_edificio'])

    # Agregar detalles de cuentas por cobrar
    y = 440
    for item in datos_factura['CXCDetalle']:
        c.drawString(90, y, str(item['cuenta']))
        c.drawString(220, y, item['descripcion'])
        c.drawString(500, y, str(item['monto']))
        y -= 20

    c.setFillColorRGB(0, 0, 0)  # Color negro
    c.setFont("PoppinsBold", 18)  # Tipografía Helvetica, tamaño de fuente 12
    # Agregar detalles de CXC
    c.drawString(392, 603, "# 0" + str(datos_factura['id_CXC']))
    c.drawString(190, 90, datos_factura['fecha_vencimiento'])
    c.drawString(490, 213, str(datos_factura['total']))

    c.setFont("PoppinsRegular", 10)  # Tipografía Helvetica, tamaño de fuente 12

    # Agregar valores de campos adicionales
    c.drawString(160, 275, datos_factura['administracion'])
    c.drawString(160, 264, datos_factura['parqueadero'])
    c.drawString(160, 253, datos_factura['retroactivo'])
    c.drawString(160, 242, datos_factura['multas'])
    c.drawString(160, 231, datos_factura['intereses'])
    c.drawString(160, 221, datos_factura['cobro_juridico'])
    c.setFillColorRGB(0, 0, 0)  # Color negro
    c.drawString(160, 209, datos_factura['total_final'])

    c.setFillColorRGB(0.17, 0.27, 0.74)  # Color Azul
    c.setFont("PoppinsRegular", 8)  # Tipografía Helvetica, tamaño de fuente 12
    # Agregar detalles de los bancos
    x_position = 80  # Posición horizontal para la información de los bancos
    for banco in datos_factura['bancos']:
        c.drawString(x_position, 160, f"Banco: {banco['banco']}")
        c.drawString(x_position, 145, f"Tipo: {banco['tipo']}")
        c.drawString(x_position, 130, f"Cuenta: {banco['cuenta']}")
        x_position += 110  # Incrementar la posición horizontal para el próximo banco

    # Guardar el PDF
    carpeta_contabilidad = "contabilidad"
    carpeta_edificio = os.path.join(carpeta_contabilidad, str(edificio_id))
    if not os.path.exists(carpeta_edificio):
        os.makedirs(carpeta_edificio)
    nombre_archivo = f"CXC{id_CXC}.pdf"
    ruta_guardado = os.path.join(carpeta_edificio, nombre_archivo)
    c.save()
    os.rename(filename, ruta_guardado)


def create_pdf_CXC(id_CXC, user_id, edificio_id):
    DATABASE = 'database.db'
    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()
    
    # Consulta para obtener los detalles del edificio
    cursor.execute("""
    SELECT nombre, nit, ciudad, nombreAMD, cedula, celular, correo, Banco1, Cuenta1, tipo1, Banco2, Cuenta2, tipo2, 
    Banco3, Cuenta3, tipo3, Banco4, Cuenta4, tipo4
    FROM Edificios 
    WHERE edificio_id = ?
    """, (edificio_id,))
    resultado_edificio = cursor.fetchone()
    
    # Consulta para obtener los detalles del propietario
    cursor.execute("""
    SELECT apto, bloque, nombres, apellidos, parq, cedula, celular, direccion, correo
    FROM Propietarios 
    WHERE edificio_id = ? AND user_id = ?
    """, (edificio_id, user_id))
    resultado_propietario = cursor.fetchone()

    # Consulta para obtener los detalles de la cuenta por cobrar
    cursor.execute("""
    SELECT id_CXC, fecha_emision, fecha_vencimiento 
    FROM CuentasCobrar 
    WHERE edificio_id = ? AND user_id = ?
    """, (edificio_id, user_id))
    resultado_cuentas_cobrar = cursor.fetchone()

    # Consulta para obtener los detalles de la cuenta por cobrar
    cursor.execute("""
    SELECT descripcion, monto, tipo
    FROM CXCDetalle 
    WHERE id_CXC = ? AND user_id = ?
    """, (id_CXC, user_id))
    resultado_detalle_cxc = cursor.fetchall()

    # Calcular el total como la suma de los montos
    total = sum(row[1] for row in resultado_detalle_cxc)

    pendiente  = {
        'administracion': '$50',
        'parqueadero': '$20',
        'retroactivo': '$30',
        'multas': '$40',
        'intereses': '$10',
        'cobro_juridico': '$20',
        'total_final': '$670'
    }

    conexion.close()
    
    # Devolver los resultados como un diccionario
    return {
        'nombre_edificio': resultado_edificio[0],
        'nit': resultado_edificio[1],
        'ciudad': resultado_edificio[2],
        'nombre_amd_edificio': resultado_edificio[3],
        'cedula_amd_edificio': resultado_edificio[4],
        'celular_amd_edificio': resultado_edificio[5],
        'correo_amd_edificio': resultado_edificio[6],
        'apto': resultado_propietario[0],
        'bloque': resultado_propietario[1],
        'nombres_propietario': resultado_propietario[2],
        'apellidos_propietario': resultado_propietario[3],
        'parq': resultado_propietario[4],
        'cedula_propietario': resultado_propietario[5],
        'celular_propietario': resultado_propietario[6],
        'direccion_propietario': resultado_propietario[7],
        'correo_propietario': resultado_propietario[8],
        'id_CXC': resultado_cuentas_cobrar[0],
        'fecha_emision': resultado_cuentas_cobrar[1],
        'fecha_vencimiento': resultado_cuentas_cobrar[2],
        'total': total,
        'CXCDetalle': [{'cuenta': "0", 'descripcion': row[0], 'monto': row[1], 'tipo': row[2]} for row in resultado_detalle_cxc],
        'bancos': [
            {'banco': resultado_edificio[7], 'tipo': resultado_edificio[9], 'cuenta': resultado_edificio[8]},
            {'banco': resultado_edificio[10], 'tipo': resultado_edificio[12], 'cuenta': resultado_edificio[11]},
            {'banco': resultado_edificio[13], 'tipo': resultado_edificio[15], 'cuenta': resultado_edificio[14]},
            {'banco': resultado_edificio[16], 'tipo': resultado_edificio[18], 'cuenta': resultado_edificio[17]}
        ],
        'administracion': pendiente['administracion'],
        'parqueadero': pendiente['parqueadero'],
        'retroactivo': pendiente['retroactivo'],
        'multas': pendiente['multas'],
        'intereses': pendiente['intereses'],
        'cobro_juridico': pendiente['cobro_juridico'],
        'total_final': pendiente['total_final']
    }



if __name__ == '__main__':
    # Iniciar la aplicación Flask
    #app.run(debug=True, port=5000)
    app.run(debug=True, host='0.0.0.0')
