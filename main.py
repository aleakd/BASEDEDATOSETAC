from flask import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user, login_manager
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ale12345678ale'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guardiaA.db'
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)


with app.app_context():
    class Agentes(db.Model):
        id_agente = db.Column(db.Integer, primary_key=True,unique=True)
        apellido = db.Column(db.String(100) )
        nombre = db.Column(db.String(100))
        guardia = db.Column(db.String(10))
        dni = db.Column(db.Integer)
        telefono = db.Column(db.Integer)
        telefono_alternativo = db.Column(db.Integer)
        Fecha_nacimiento = db.Column(db.Date)
        localidad = db.Column(db.String(100))
        domicilio = db.Column(db.String(300))
        email = db.Column(db.String(100))
        Rol = db.Column(db.String(100))
        Alergia = db.Column(db.String(100))
        Camada = db.Column(db.String(10))
        Bombero = db.Column(db.String(1000))
        registro= db.Column(db.String(1000))
    #Line below only required once, when creating DB.
    db.create_all()

with app.app_context():
    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        name = db.Column(db.String(1000))
        telefono = db.Column(db.String(15))
    #Line below only required once, when creating DB.
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
    class Cambiosguardia(db.Model):
        __tablename__ = 'Cambiosguardia'  # Agrega esta línea para especificar el nombre de la tabla en la base de datos
        id_agente = db.Column(db.Integer, primary_key=True)
        fecha_de_ausencia = db.Column(db.Date)
        Id_agente_cubre = db.Column(db.Integer)
        fecha_devolucion = db.Column(db.Date)
        Motivo = db.Column(db.String(1000))




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

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
            #aca podria ir la tabla de reigistro de cada agente admin


            return redirect(url_for("secrets"))
    return render_template("login.html")





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

        return redirect(url_for("secrets.html"))
    return render_template("register.html")


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
                fechaoven= datetime.strptime(fecha_ven, '%Y-%m-%d').date()
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

    ultimos3_usuarios = User.query.order_by(User.id.desc()).limit(3).all()
    print(current_user.name)
    return render_template("secrets.html", name=current_user, last_three_users=ultimos3_usuarios)






@app.route('/guardiaA', methods=["GET", "POST"])
@login_required
def guardiaA():
    agentesA = Agentes.query.filter(Agentes.guardia == 'A').order_by(Agentes.id_agente).all()
    return render_template("guardiaA.html", lista_agentes=agentesA)

@app.route('/licencias_A', methods=["GET", "POST"])
@login_required
def licenciasA():
    agentesA = Agentes.query.filter(Agentes.guardia == 'A').order_by(Agentes.id_agente).all()
    licenciasA= CarnetConducir.query.order_by(CarnetConducir.id_agente).all()
    return render_template("licenciasa.html", lista_agentes=agentesA, Licencias=licenciasA)






@app.route('/guardiaB', methods=["GET", "POST"])
@login_required
def guardiaB():
    agentesB = Agentes.query.filter(Agentes.guardia == 'B').order_by(Agentes.id_agente).all()
    return render_template("guardiaB.html", lista_agentes=agentesB)

@app.route('/licencias_B', methods=["GET", "POST"])
@login_required
def licenciasB():
    agentesB = Agentes.query.filter(Agentes.guardia == 'B').order_by(Agentes.id_agente).all()
    licenciasB= CarnetConducir.query.order_by(CarnetConducir.id_agente).all()
    return render_template("licenciasb.html", lista_agentes=agentesB, Licencias=licenciasB)






@app.route('/guardiaC', methods=["GET", "POST"])
@login_required
def guardiaC():
    agentesC = Agentes.query.filter(Agentes.guardia == 'C').order_by(Agentes.id_agente).all()
    return render_template("guardiaC.html", lista_agentes=agentesC)

@app.route('/licencias_C', methods=["GET", "POST"])
@login_required
def licenciasC():
    agentesC = Agentes.query.filter(Agentes.guardia == 'C').order_by(Agentes.id_agente).all()
    licenciasC= CarnetConducir.query.order_by(CarnetConducir.id_agente).all()
    return render_template("licenciasC.html", lista_agentes=agentesC, Licencias=licenciasC)




@app.route('/moviles')
def moviles():
    return render_template("moviles.html")








if __name__ == '__main__':
    app.run(debug=True, port=8080)  # Cambia 8080 al puerto que prefieras
