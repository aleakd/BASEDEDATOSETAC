from flask import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user, login_manager
from datetime import datetime
import pytz
from pytz import timezone
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

#-------------------------------------------------------------------------------



app = Flask(__name__)
app.config['TIMEZONE'] = pytz.timezone('America/Argentina/Buenos_Aires')
app.config['SECRET_KEY'] = 'ale12345678ale'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guardiaA.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


#------------------------------------------




# TABLAS EN BASE DE DATOS:

with app.app_context():
    class Agentes(db.Model):
        id_agente = db.Column(db.Integer, primary_key=True, unique=True)
        apellido = db.Column(db.String(100))
        nombre = db.Column(db.String(100))
        guardia = db.Column(db.String(10))
        base = db.Column(db.String(15))
        dni = db.Column(db.Integer)
        telefono = db.Column(db.Integer)
        telefono_alternativo = db.Column(db.Integer)
        Fecha_nacimiento = db.Column(db.Date)
        localidad = db.Column(db.String(100))
        domicilio = db.Column(db.String(300))
        email = db.Column(db.String(100))
        Rol = db.Column(db.String(100))
        Grupo_sanguineo = db.Column(db.String(100))
        Alergia = db.Column(db.String(100))
        Camada = db.Column(db.String(10))
        Bombero = db.Column(db.String(1000))
        registro = db.Column(db.String(1000))


    # Line below only required once, when creating DB.
    db.create_all()






with app.app_context():
    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        name = db.Column(db.String(1000))
        telefono = db.Column(db.String(15))


    # Line below only required once, when creating DB.
    db.create_all()




with app.app_context():
    class CarnetConducir(db.Model):
        __tablename__ = 'CarnetConducir'  # Agrega esta línea para especificar el nombre de la tabla en la base de datos
        id_agente = db.Column(db.Integer, primary_key=True, unique=True)
        Tipo = db.Column(db.String(100))
        fecha_otorg = db.Column(db.Date)
        fecha_vencim = db.Column(db.Date)
        Observacion = db.Column(db.String(1000))





with app.app_context():
    class Talles(db.Model):
        __tablename__ = 'Talles'  # Agrega esta línea para especificar el nombre de la tabla en la base de datos
        id_agente = db.Column(db.Integer, primary_key=True, unique=True)
        Remer_gris = db.Column(db.String(10))
        Borcegos = db.Column(db.Integer)
        Pantalon_gris = db.Column(db.String(10))
        Chaqueta_forestal = db.Column(db.String(10))
        Pantalon_forestal = db.Column(db.String(10))
        Guantes = db.Column(db.Integer)
        Buzo = db.Column(db.String(10))
        Campera = db.Column(db.String(10))


with app.app_context():
    class Provistos(db.Model):
        __tablename__ = 'Provistos'
        id_agente = db.Column(db.Integer, primary_key=True)
        borcegos = db.Column(db.Integer)
        remera = db.Column(db.Integer)
        pantalon_fajina = db.Column(db.Integer)
        campera_celeste = db.Column(db.Integer)
        campera_roja = db.Column(db.Integer)
        buzo_celeste = db.Column(db.Integer)
        gorra = db.Column(db.Integer)
        pantalon_forestal = db.Column(db.Integer)
        camisa_forestal = db.Column(db.Integer)
        remera_primerapiel = db.Column(db.Integer)
        guantes = db.Column(db.Integer)
        casco = db.Column(db.Integer)
        monja = db.Column(db.Integer)
        antiparras = db.Column(db.Integer)
        linterna = db.Column(db.Integer)
        mochila_nawan = db.Column(db.Integer)
        bomba_espalda = db.Column(db.Integer)








with app.app_context():
    class Cambiosguardia(db.Model):
        __tablename__ = 'Cambiosguardia'  # Agrega esta línea para especificar el nombre de la tabla en la base de datos
        id_cambio = db.Column(db.Integer, primary_key=True)
        id_agente = db.Column(db.Integer)
        fecha_de_ausencia = db.Column(db.Date)
        Id_agente_cubre = db.Column(db.Integer)
        fecha_devolucion = db.Column(db.Date)
        Motivo = db.Column(db.String(1000))




with app.app_context():
    class Movimientos_moviles(db.Model):
        __tablename__ = 'Movimientos_moviles'  # Agrega esta línea para especificar el nombre de la tabla en la base de datos
        id_movimiento = db.Column(db.Integer, primary_key=True)
        fecha = db.Column(db.Date)
        numero_movil = db.Column(db.Integer)
        destino = db.Column(db.String(1000))
        hora_salida = db.Column(db.Time)
        km_salida = db.Column(db.Integer)
        hora_llegada = db.Column(db.Time)
        km_llegada = db.Column(db.Integer)
        a_cargo = db.Column(db.String(50))
        chofer = db.Column(db.String(50))
        novedades = db.Column(db.String(100))


with app.app_context():
    class Comisiones(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        fecha = db.Column(db.Date)
        hora = db.Column(db.String(100))
        nmovil = db.Column(db.Integer)
        ag_cargo = db.Column(db.String(100))
        ag_chofer = db.Column(db.String(100))
        dotacion = db.Column(db.String(100))
        destino = db.Column(db.String(100))
        odometro = db.Column(db.Integer)
        novedades = db.Column(db.String(300))


    db.create_all()




with app.app_context():
    class Salida(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        fecha = db.Column(db.Date)
        nmovil = db.Column(db.String(100))
        ag_cargo = db.Column(db.String(100))
        ag_chofer = db.Column(db.String(100))
        dotacion = db.Column(db.String(100))
        zona = db.Column(db.String(100))
        handys = db.Column(db.String(100))
        gorgi = db.Column(db.Integer)
        pulasky = db.Column(db.Integer)
        pala = db.Column(db.Integer)
        mclood = db.Column(db.Integer)
        derqui = db.Column(db.Integer)
        bidon_nafta = db.Column(db.Integer)
        bolsa_rescate = db.Column(db.String(100))
        torpedo = db.Column(db.Integer)
        tabla = db.Column(db.Integer)
        conos = db.Column(db.Integer)
        sopladora = db.Column(db.String(100))
        cajon = db.Column(db.String(100))
        chaleco = db.Column(db.Integer)
        odometro = db.Column(db.Integer)
        bolsos_trauma = db.Column(db.Integer)
        herramienta_adicional = db.Column(db.String(100))
        hora = db.Column(db.String(100))


    db.create_all()




with app.app_context():
    class Parte_inter(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        num_movil = db.Column(db.String(20))
        ag_responsable = db.Column(db.String(50))
        dotacion = db.Column(db.String(50))
        fecha_arribo = db.Column(db.Date)
        hora_arribo = db.Column(db.Time)
        fecha_finalizacion = db.Column(db.Date)
        hora_finalizacion = db.Column(db.Time)
        tipo_intervencion = db.Column(db.String(50))
        calle_altura = db.Column(db.String(100))
        comuna_municipio = db.Column(db.String(100))
        acceso_lugar = db.Column(db.String(100))
        sup_afectada = db.Column(db.String(50))
        material_combustible = db.Column(db.String(50))
        viviendas = db.Column(db.String(50))
        vehiculos = db.Column(db.String(50))
        personal_salud = db.Column(db.String(100))
        personal_policial = db.Column(db.String(100))
        personal_bomberos = db.Column(db.String(100))
        defensa_civil = db.Column(db.String(100))
        otro_equipo = db.Column(db.String(100))
        personal_lesionado = db.Column(db.String(100))
        resumen = db.Column(db.String(500))

    db.create_all()

with app.app_context():
    class Asistencias(db.Model):
        __tablename__ = 'asistencias'
        id_asistencia = db.Column(db.Integer, primary_key=True)
        Id_agente = db.Column(db.Integer)
        fecha = db.Column(db.Date)
        hora = db.Column(db.String(10))
        almuerza = db.Column(db.String(10))
        cena = db.Column(db.String(10))


    db.create_all()






#--------------------FIN DE TABLAS DE DATOS-----------------------------------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#----------------------------------------------


@app.route('/', methods=['GET', 'POST'])
def index():
    resultados_consulta = db.session.query(
        Movimientos_moviles.numero_movil,
        db.func.max(Movimientos_moviles.id_movimiento).label('last_id'),
        Movimientos_moviles.km_salida,
        Movimientos_moviles.km_llegada
    ).group_by(Movimientos_moviles.numero_movil).order_by(Movimientos_moviles.numero_movil).all()

    if request.method == 'POST':

        if 'registro_movil' in request.form:
            fecha = datetime.strptime(request.form['fecha'],
                                      '%Y-%m-%d').date()  # Convierte la cadena de fecha a objeto de fecha
            movil = request.form['movil']
            destino = request.form['destino_actividad']


            # Obtén el km_salida desde la última entrada en Salida para el nmovil dado
            nmovil = request.form['movil']
            ultima_salida = Salida.query.filter_by(nmovil=nmovil).order_by(Salida.id.desc()).first()
            km_salida = ultima_salida.odometro if ultima_salida else None

            km_llegada = request.form['km_llegada']
            hora_llegada = datetime.strptime(request.form['hora_llegada'],
                                             '%H:%M').time()  # Convierte la cadena de hora a objeto de hora
            hora_salida = datetime.strptime(request.form['hora_salida'], '%H:%M').time()
            novedades=request.form['novedades']

            nuevo_registro = Movimientos_moviles(
                fecha=fecha,
                numero_movil=movil,
                destino=destino,
                km_salida=km_salida,
                km_llegada=km_llegada,
                hora_llegada=hora_llegada,
                hora_salida=hora_salida,
                a_cargo=request.form.get('a_cargo').upper(),
                chofer=request.form.get('chofer').upper(),
                novedades=novedades
            )



            db.session.add(nuevo_registro)
            db.session.commit()
            flash('Se registro correctamente el movimiento del movil')


        if 'parte_salida' in request.form:

            nmovil = request.form.get('nmovil')
            ag_cargo = request.form.get('ag_cargo').upper()
            ag_chofer = request.form.get('ag_chofer')
            dotacion = request.form.get('dotacion')
            zona = request.form.get('zona')

            handys = request.form.get('handys')  # Obtén el valor del campo "handys" como una cadena
            handys_list = [h.strip() for h in handys.split(',')]  # Divide los números por comas y crea una lista
            handys_str = ','.join(handys_list)  # Convierte la lista en una cadena separada por comas

            gorgi = request.form.get('gorgi')
            pulasky = request.form.get('pulasky')
            pala = request.form.get('pala')
            mclood = request.form.get('mclood')
            derqui = request.form.get('derqui')
            bidon_nafta = request.form.get('bidon_nafta')

            bolsa_rescate = request.form.get('bolsa_rescate')
            bolsa_rescate_list = [h.strip() for h in bolsa_rescate.split(',')]
            bolsa_rescate_str = ','.join(bolsa_rescate_list)

            torpedo = request.form.get('torpedo')
            tabla = request.form.get('tabla')
            conos = request.form.get('conos')
            sopladora = request.form.get('Sopladora')
            cajon = request.form.get('cajon')
            chaleco = request.form.get('chaleco')
            odometro = request.form.get('odometro')
            bolsos_trauma = request.form.get('bolsos_trauma')
            herramienta_adicional = request.form.get('herramienta_adicional')
            fecha_actual = datetime.now().date()
            hora_actual_utc = datetime.now(timezone('UTC'))
            hora_actual_buenos_aires = hora_actual_utc.astimezone(app.config['TIMEZONE'])


            # Crea una nueva entrada en la base de datos
            nueva_salida = Salida(
                fecha=fecha_actual,
                nmovil=nmovil,
                ag_cargo=ag_cargo,
                ag_chofer=ag_chofer,
                dotacion=dotacion,
                zona=zona,
                handys=handys_str,
                gorgi=gorgi,
                pulasky=pulasky,
                pala=pala,
                mclood=mclood,
                derqui=derqui,
                bidon_nafta=bidon_nafta,
                bolsa_rescate=bolsa_rescate_str,
                torpedo=torpedo,
                tabla=tabla,
                conos=conos,
                sopladora=sopladora,
                cajon=cajon,
                chaleco=chaleco,
                odometro=odometro,
                bolsos_trauma=bolsos_trauma,
                herramienta_adicional=herramienta_adicional,
                hora=hora_actual_buenos_aires.strftime('%H:%M')

            )

            db.session.add(nueva_salida)
            db.session.commit()
            flash("Parte de salida registrado correctamente")

        if 'salida_comision' in request.form:
            fecha_actual = datetime.now().date()
            nmovil = request.form.get('nmovil')
            ag_cargo = request.form.get('ag_cargo').upper()
            ag_chofer = request.form.get('ag_chofer')
            dotacion = request.form.get('dotacion')
            destino = request.form.get('destino')
            odometro = request.form.get('odometro')
            novedades = request.form.get('novedades')
            hora_actual_utc = datetime.now(timezone('UTC'))
            hora_actual_buenos_aires = hora_actual_utc.astimezone(app.config['TIMEZONE'])

            nueva_salida = Salida(
                fecha=fecha_actual,
                nmovil=nmovil,
                ag_cargo=ag_cargo,
                ag_chofer=ag_chofer,
                dotacion=dotacion,
                zona=destino,
                handys=0,
                gorgi=0,
                pulasky=0,
                pala=0,
                mclood=0,
                derqui=0,
                bidon_nafta=0,
                bolsa_rescate=0,
                torpedo=0,
                tabla=0,
                conos=0,
                sopladora=0,
                cajon=0,
                chaleco=0,
                odometro=odometro,
                bolsos_trauma=0,
                herramienta_adicional=novedades,
                hora=hora_actual_buenos_aires.strftime('%H:%M')

            )


            comision = Comisiones(
                fecha = fecha_actual,
                hora = hora_actual_buenos_aires.strftime('%H:%M'),
                nmovil= nmovil,
                ag_cargo = ag_cargo,
                ag_chofer = ag_chofer,
                dotacion = dotacion,
                destino = destino,
                odometro = odometro,
                novedades = novedades
            )
            db.session.add(nueva_salida)
            db.session.commit()
            flash("Parte de salida registrado correctamente")


    return render_template("index.html", moviles=movimientos, ultimos=resultados_consulta)

#----------------------------------------------


@app.route('/asistencias', methods=['GET', 'POST'])
def asistencias():
    fecha_actual = datetime.now().date()
    hora_actual_utc = datetime.now(timezone('UTC'))
    hora_actual_buenos_aires = hora_actual_utc.astimezone(app.config['TIMEZONE'])
    hora_actual_str = hora_actual_buenos_aires.strftime('%H:%M')

    if request.method == 'POST':
        dni_agente = request.form.get('dni_agente')

        # Verificar si el agente existe en la tabla Agentes
        agente_existente = Agentes.query.filter_by(dni=dni_agente).first()

        if not agente_existente:
            flash('No se puede registrar la asistencia. El DNI no está registrado.')
            return redirect(url_for("index"))

        # Verificar si el agente ya se registró hoy
        asistencia_existente = (
            Asistencias.query
            .filter(Asistencias.Id_agente == dni_agente, Asistencias.fecha == fecha_actual)
            .first()
        )

        if asistencia_existente:
            flash('El agente ya se registró hoy. No puede registrar múltiples veces en el mismo día.')
            return redirect(url_for("index"))

        almuerza = request.form['almuerza']




        asistencia = Asistencias(
            Id_agente=dni_agente,
            fecha=fecha_actual,
            hora=hora_actual_str,
            almuerza=almuerza,

        )
        db.session.add(asistencia)
        db.session.commit()
        flash('Asistencia cargada exitosamente')


        return redirect(url_for("index"))

    # Esto se ejecuta si la solicitud es GET
    asistencias_del_dia = Asistencias.query.filter(Asistencias.fecha == fecha_actual).all()
    todos_los_agentes = Agentes.query.order_by(Agentes.id_agente).all()
    almuerza_si_count = Asistencias.query.filter(Asistencias.almuerza == 'SI', Asistencias.fecha == fecha_actual).count()
    cena_si_count = Asistencias.query.filter(Asistencias.cena == 'SI', Asistencias.fecha == fecha_actual).count()

    cambioguardia = Cambiosguardia.query.filter((Cambiosguardia.fecha_de_ausencia == fecha_actual) | (
                Cambiosguardia.fecha_devolucion == fecha_actual)).order_by(Cambiosguardia.id_cambio).all()

    return render_template("asistencias.html", asistencias=asistencias_del_dia, agentee=todos_los_agentes, almuerza_si_count=almuerza_si_count, cena_si_count=cena_si_count,
                           cambioguar=cambioguardia)







#----------------------------------------------

@app.route('/movimientos')
def movimientos():
    movimientos = Movimientos_moviles.query.order_by(Movimientos_moviles.id_movimiento).all()

    return render_template("movimientos.html", moviles=movimientos)


#----------------------------------------------


@app.route('/registrar_parte', methods=['GET', 'POST'])
def registrar_parte():
    if request.method == 'POST':
        num_movil = request.form['num-movil']
        ag_responsable = request.form['ag_responsable']
        dotacion = request.form['dotacion']
        fecha_arribo = datetime.strptime(request.form['fecha_arribo'], '%Y-%m-%d')
        hora_arribo = datetime.strptime(request.form['hora_arribo'], '%H:%M').time()
        fecha_finalizacion = datetime.strptime(request.form['fecha_finalizacion'], '%Y-%m-%d')
        hora_finalizacion = datetime.strptime(request.form['hora_finalizacion'], '%H:%M').time()
        tipo_intervencion = request.form['tipo_intervencion']
        calle_altura = request.form['calle_altura']
        comuna_municipio = request.form['comuna_municipio']
        acceso_lugar = request.form['acceso_lugar']
        sup_afectada = request.form['sup_afectada']
        material_combustible = request.form['material_combustible']
        viviendas = request.form['viviendas']
        vehiculos = request.form['vehiculos']
        personal_salud = request.form['personal_salud']
        personal_policial = request.form['personal_policial']
        personal_bomberos = request.form['personal_bomberos']
        defensa_civil = request.form['defensa_civil']
        otro_equipo = request.form['otro_equipo']
        personal_lesionado = request.form['personal_lesionado']
        resumen = request.form['resumen']

        intervencion = Parte_inter(
            num_movil=num_movil,
            ag_responsable=ag_responsable.upper(),
            dotacion=dotacion.upper(),
            fecha_arribo=fecha_arribo,
            hora_arribo=hora_arribo,
            fecha_finalizacion=fecha_finalizacion,
            hora_finalizacion=hora_finalizacion,
            tipo_intervencion=tipo_intervencion,
            calle_altura=calle_altura,
            comuna_municipio=comuna_municipio,
            acceso_lugar=acceso_lugar,
            sup_afectada=sup_afectada,
            material_combustible=material_combustible,
            viviendas=viviendas,
            vehiculos=vehiculos,
            personal_salud=personal_salud,
            personal_policial=personal_policial,
            personal_bomberos=personal_bomberos,
            defensa_civil=defensa_civil,
            otro_equipo=otro_equipo,
            personal_lesionado=personal_lesionado,
            resumen=resumen
        )

        db.session.add(intervencion)
        db.session.commit()

    return render_template("registrar_parte.html")

#----------------------------------------------


@app.route('/partes', methods=['GET', 'POST'])
def partes():
    registros = Parte_inter.query.order_by(Parte_inter.id.desc()).all()
    return render_template("partes.html", registros=registros)

#----------------------------------------------



@app.route('/salidas', methods=['GET', 'POST'])
def salidas():
    if request.method == 'POST':
        id_filtro = request.form['id_filtro']
    else:
        salidas = Salida.query.order_by(Salida.id.desc()).all()
        comision= Comisiones.query.order_by(Comisiones.id.desc()).all()
    return render_template('salidas.html', salidas=salidas, comisiones=comision)


#----------------------------------------------



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("usuario no encontrado")
            return redirect(url_for('login'))

        elif not check_password_hash(user.password, password):
            flash("Contraseña incorrecta")
            return redirect(url_for('login'))
        else:

            login_user(user)
            # aca podria ir la tabla de reigistro de cada agente admin

            return redirect(url_for("secrets"))
    return render_template("login.html")


#----------------------------------------------


@app.route('/register', methods=["GET", "POST"])
@login_required
def register():
    if request.method == "POST":
        hash_password = generate_password_hash(request.form.get("password"),
                                               method='pbkdf2:sha256',
                                               salt_length=6)
        new_user = User(
            email=request.form.get("email"),
            name=request.form.get("name"),
            password=hash_password,
            telefono=request.form.get("telefono")
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("secrets"))
    return render_template("register.html")


#----------------------------------------------


@app.route('/secrets', methods=["GET", "POST"])
@login_required
def secrets():
    if request.method == "POST":
        if 'registrar_agente' in request.form:
            # Convertir las cadenas de fecha en objetos de fecha (date) de Python
            fecha_ins_str = request.form.get("nacimiento")
            try:
                nacimiento = datetime.strptime(fecha_ins_str, '%Y-%m-%d').date()
            except ValueError:
                flash(
                    "Error: Formato de fecha incorrecto. Asegúrate de que las fechas estén en el formato 'YYYY-MM-DD'")
                # Aquí puedes decidir cómo manejar el error, ya sea lanzando una excepción, mostrando un mensaje de error o realizando alguna otra acción apropiada.
                return redirect(url_for("secrets"))

            nuevo_agente = Agentes(
                apellido=request.form.get("apellido"),
                nombre=request.form.get("nombre"),
                guardia=request.form.get("guardia"),
                dni=request.form.get("dni"),
                telefono=request.form.get("telefono"),
                telefono_alternativo=request.form.get("telefono_alter"),
                Fecha_nacimiento=nacimiento,
                localidad=request.form.get("localidad"),
                domicilio=request.form.get("domicilio"),
                email=request.form.get("email"),
                Rol=request.form.get("rol"),
                Grupo_sanguineo=request.form.get("grupo_sanguineo"),
                Alergia=request.form.get("alergia"),
                Camada=request.form.get("camada"),
                Bombero=request.form.get("bombero"),
                registro=current_user.name
            )

            db.session.add(nuevo_agente)
            db.session.commit()
            flash("Se registró correctamente la información del Agente")

        if 'registrar_carnet' in request.form:
            # Convertir las cadenas de fecha en objetos de fecha (date) de Python
            fecha_oto = request.form.get("fecha_otor")
            fecha_ven = request.form.get("fecha_venc")
            try:
                fechaotor = datetime.strptime(fecha_oto, '%Y-%m-%d').date()
                fechaoven = datetime.strptime(fecha_ven, '%Y-%m-%d').date()
            except ValueError:
                flash(
                    "Error: Formato de fecha incorrecto. Asegúrate de que las fechas estén en el formato 'YYYY-MM-DD'")
                # Aquí puedes decidir cómo manejar el error, ya sea lanzando una excepción, mostrando un mensaje de error o realizando alguna otra acción apropiada.
                return redirect(url_for("secrets"))

            nueva_licencia = CarnetConducir(
                id_agente=request.form.get("id_agente"),
                Tipo=request.form.get("tipo"),
                fecha_otorg=fechaotor,
                fecha_vencim=fechaoven,
                Observacion=request.form.get("observacion")
            )
            db.session.add(nueva_licencia)
            db.session.commit()
            flash("Se registró correctamente el Carnet")

        if "registrar_talles" in request.form:
            nuevo_talle = Talles(
                id_agente=request.form.get("id_agente"),
                Remer_gris=request.form.get("remera_gris"),
                Borcegos=request.form.get("borcegos"),
                Pantalon_gris=request.form.get("pantalon_gris"),
                Chaqueta_forestal=request.form.get("chaqueta_forestal"),
                Pantalon_forestal=request.form.get("pantalon_forestal"),
                Guantes=request.form.get("guantes"),
                Buzo=request.form.get("buzo"),
                Campera=request.form.get("campera")

            )
            db.session.add(nuevo_talle)
            db.session.commit()
            flash("Se registraron correctamente los talles solicitados ")

        if "cambiosguardia" in request.form:
            # Convertir las cadenas de fecha en objetos de fecha (date) de Python
            fecha_aus = request.form.get("fecha_ausencia")
            fecha_dev = request.form.get("fecha_devolucion")
            try:
                fechaause = datetime.strptime(fecha_aus, '%Y-%m-%d').date()
                fechadevo = datetime.strptime(fecha_dev, '%Y-%m-%d').date()
            except ValueError:
                flash(
                    "Error: Formato de fecha incorrecto. Asegúrate de que las fechas estén en el formato 'YYYY-MM-DD'")
                # Aquí puedes decidir cómo manejar el error, ya sea lanzando una excepción, mostrando un mensaje de error o realizando alguna otra acción apropiada.
                return redirect(url_for("secrets"))
            nuevo_cambio = Cambiosguardia(
                id_agente=request.form.get("id_agente"),
                fecha_de_ausencia=fechaause,
                Id_agente_cubre=request.form.get("id_agente_cubre"),
                fecha_devolucion=fechadevo,
                Motivo=request.form.get("motivo")
            )
            db.session.add(nuevo_cambio)
            db.session.commit()
            flash("Se registro el cambio de guardia ")

        if "equipamiento" in request.form:
            nuevo_equipamiento = Provistos(
                id_agente=request.form.get("id_agente"),
                borcegos=request.form.get("borcegos"),
                remera=request.form.get("remera_gris"),
                pantalon_fajina=request.form.get("pantalon_fajina"),
                campera_celeste=request.form.get("campera_celeste"),
                campera_roja=request.form.get("campera_roja"),
                buzo_celeste=request.form.get("buzo_celeste"),
                gorra=request.form.get("gorra"),
                pantalon_forestal=request.form.get("pantalon_forestal"),
                camisa_forestal=request.form.get("camisa_forestal"),
                remera_primerapiel=request.form.get("remera_primerapiel"),
                guantes=request.form.get("guantes"),
                casco=request.form.get("casco"),
                monja=request.form.get("monja"),
                antiparras=request.form.get("antiparras"),
                linterna=request.form.get("linterna"),
                mochila_nawan=request.form.get("mochila_nawan"),
                bomba_espalda=request.form.get("bomba_espalda")

            )

            db.session.add(nuevo_equipamiento)
            db.session.commit()
            flash("Se registró correctamente el equipamiento")

    ultimos3_usuarios = User.query.order_by(User.id.desc()).all()
    print(current_user.name)
    return render_template("secrets.html", name=current_user, last_three_users=ultimos3_usuarios)


#----------------------------------------------


@app.route('/guardiaA', methods=["GET", "POST"])
@login_required
def guardiaA():
    agentesA = Agentes.query.filter(Agentes.guardia == 'A').order_by(Agentes.id_agente).all()
    return render_template("guardiaA.html", lista_agentes=agentesA)


@app.route('/licencias_A', methods=["GET", "POST"])
@login_required
def licenciasA():
    agentesA = Agentes.query.filter(Agentes.guardia == 'A').order_by(Agentes.id_agente).all()
    licenciasA = CarnetConducir.query.order_by(CarnetConducir.id_agente).all()
    return render_template("licenciasa.html", lista_agentes=agentesA, Licencias=licenciasA)


@app.route('/talles_A', methods=["GET", "POST"])
@login_required
def tallesA():
    agentesA = Agentes.query.filter(Agentes.guardia == 'A').order_by(Agentes.id_agente).all()
    provistosA = Talles.query.order_by(Talles.id_agente).all()
    equipamiento = Provistos.query.order_by(Provistos.id_agente).all()
    return render_template("provistosa.html", lista_agentes=agentesA, provistos=provistosA, equipa=equipamiento)


#----------------------------------------------


@app.route('/guardiaB', methods=["GET", "POST"])
@login_required
def guardiaB():
    agentesB = Agentes.query.filter(Agentes.guardia == 'B').order_by(Agentes.id_agente).all()
    return render_template("guardiaB.html", lista_agentes=agentesB)


@app.route('/licencias_B', methods=["GET", "POST"])
@login_required
def licenciasB():
    agentesB = Agentes.query.filter(Agentes.guardia == 'B').order_by(Agentes.id_agente).all()
    licenciasB = CarnetConducir.query.order_by(CarnetConducir.id_agente).all()
    return render_template("licenciasb.html", lista_agentes=agentesB, Licencias=licenciasB)


@app.route('/talles_B', methods=["GET", "POST"])
@login_required
def tallesB():
    agentesB = Agentes.query.filter(Agentes.guardia == 'B').order_by(Agentes.id_agente).all()
    provistosB = Talles.query.order_by(Talles.id_agente).all()
    equipamiento = Provistos.query.order_by(Provistos.id_agente).all()
    return render_template("provistosb.html", lista_agentes=agentesB, provistos=provistosB, equipa=equipamiento)



#----------------------------------------------


@app.route('/guardiaC', methods=["GET", "POST"])
@login_required
def guardiaC():
    agentesC = Agentes.query.filter(Agentes.guardia == 'C').order_by(Agentes.id_agente).all()
    return render_template("guardiaC.html", lista_agentes=agentesC)


@app.route('/licencias_C', methods=["GET", "POST"])
@login_required
def licenciasC():
    agentesC = Agentes.query.filter(Agentes.guardia == 'C').order_by(Agentes.id_agente).all()
    licenciasC = CarnetConducir.query.order_by(CarnetConducir.id_agente).all()
    return render_template("licenciasc.html", lista_agentes=agentesC, Licencias=licenciasC)


@app.route('/talles_C', methods=["GET", "POST"])
@login_required
def tallesC():
    agentesC = Agentes.query.filter(Agentes.guardia == 'C').order_by(Agentes.id_agente).all()
    provistosC = Talles.query.order_by(Talles.id_agente).all()
    equipamiento = Provistos.query.order_by(Provistos.id_agente).all()
    return render_template("provistosc.html", lista_agentes=agentesC, provistos=provistosC, equipa=equipamiento)


#----------------------------------------------
@app.route('/guardiaD', methods=["GET", "POST"])
@login_required
def guardiaD():
    agentesD = Agentes.query.filter(Agentes.guardia == 'D').order_by(Agentes.id_agente).all()
    return render_template("guardiaD.html", lista_agentes=agentesD)


@app.route('/licencias_D', methods=["GET", "POST"])
@login_required
def licenciasD():
    agentesD = Agentes.query.filter(Agentes.guardia == 'D').order_by(Agentes.id_agente).all()
    licenciasD = CarnetConducir.query.order_by(CarnetConducir.id_agente).all()
    return render_template("licenciasD.html", lista_agentes=agentesD, Licencias=licenciasD)


@app.route('/talles_D', methods=["GET", "POST"])
@login_required
def tallesD():
    agentesD = Agentes.query.filter(Agentes.guardia == 'D').order_by(Agentes.id_agente).all()
    provistosD = Talles.query.order_by(Talles.id_agente).all()
    equipamiento = Provistos.query.order_by(Provistos.id_agente).all()
    return render_template("provistosD.html", lista_agentes=agentesD, provistos=provistosD, equipa=equipamiento)
#----------------------------------------------


@app.route('/editar_licencia/<int:id_agente>', methods=['GET', 'POST'])
@login_required
def editar_licencia(id_agente):
    licencia = CarnetConducir.query.filter_by(id_agente=id_agente).first()

    if request.method == 'POST':
        fecha_otorgamiento = request.form.get('fecha_otorgamiento')
        fecha_vencimiento = request.form.get('fecha_vencimiento')

        # Validar y actualizar las fechas de otorgamiento y vencimiento
        try:
            fecha_otorgamiento = datetime.strptime(fecha_otorgamiento, '%Y-%m-%d').date()
            fecha_vencimiento = datetime.strptime(fecha_vencimiento, '%Y-%m-%d').date()
            licencia.fecha_otorg = fecha_otorgamiento
            licencia.fecha_vencim = fecha_vencimiento
            db.session.commit()
            flash('Licencia actualizada con éxito', 'success')
            return redirect(url_for('licenciasA'))  # Redirige a la página de licencias
        except ValueError:
            flash('Formato de fecha incorrecto', 'error')

    return render_template('editar_licencia.html', licencia=licencia)


#----------------------------------------------

@app.route('/moviles')
def moviles():
    return render_template("moviles.html")


#----------------------------------------------


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#----------------------------------------------

from flask import send_file

#----------------------------------------------
def obtener_registro_por_id(id):
    return Parte_inter.query.get(id)
#----------------------------------------------
def create_pdf(registro, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    # Define styles
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    style_heading = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontSize=15,
        spaceAfter=12
    )
    # Add title
    title = Paragraph("Parte de Intervención - ETAC - Calamuchita 2024", style_heading)
    elements.append(title)
    # Prepare data for PDF
    data = {
        "Id": registro.id,
        "Número de Móvil": registro.num_movil,
        "Agente Responsable": registro.ag_responsable,
        "Dotación": registro.dotacion,
        "Fecha Arribo": registro.fecha_arribo,
        "Hora Arribo": registro.hora_arribo,
        "Fecha Finalización": registro.fecha_finalizacion,
        "Hora Finalización": registro.hora_finalizacion,
        "Tipo de Intervención": registro.tipo_intervencion,
        "Calle y Altura": registro.calle_altura,
        "Comuna/Municipio/Paraje": registro.comuna_municipio,
        "Acceso al Lugar": registro.acceso_lugar,
        "Superficie Afectada": registro.sup_afectada,
        "Material Combustible": registro.material_combustible,
        "Viviendas": registro.viviendas,
        "Vehículos": registro.vehiculos,
        "Personal de Salud": registro.personal_salud,
        "Personal Policial": registro.personal_policial,
        "Personal de Bomberos": registro.personal_bomberos,
        "Defensa Civil": registro.defensa_civil,
        "Otro Equipo": registro.otro_equipo,
        "Personal Lesionado": registro.personal_lesionado,
        "Resumen": registro.resumen
    }
    # Add data to PDF
    for key, value in data.items():
        line = f"<b>{key}:</b> {value}"
        p = Paragraph(line, style_normal)
        elements.append(p)
    # Add space before the signature section
    elements.append(Spacer(1, 20))  # Ajusta el espacio vertical si es necesario

    # Add signature section
    signature_lines = """
    <br/><br/>
    FIRMA: __________________________<br/><br/>
    ACLARACIÓN: __________________________<br/><br/>
    DNI: __________________________
    """
    signature_section = Paragraph(signature_lines, style_normal)
    elements.append(signature_section)




    # Build PDF
    doc.build(elements)


#----------------------------------------------

@app.route('/generar_pdf/<int:id>', methods=['GET'])
@login_required
def generar_pdf(id):
    registro = obtener_registro_por_id(id)
    if not registro:
        abort(404)  # Si el registro no se encuentra, devuelve un error 404

    buffer = io.BytesIO()
    create_pdf(registro, buffer)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f'parte_intervencion_{id}.pdf',
                     mimetype='application/pdf')

#----------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=8080)  # Cambia 8080 al puerto que prefieras