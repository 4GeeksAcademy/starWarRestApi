"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for,render_template
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personajes, Planetas, Favoritos
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required



#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False



db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

app.config['JWT_SECRET_KEY'] = "harryPother"
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Ruta para obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_serialized = [user.serialize() for user in users]
    return jsonify(users_serialized), 200

# Ruta para obtener un usuario por ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.serialize()), 200
    else:
        return jsonify({"message": "User not found"}), 404

# Ruta para crear un nuevo usuario
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(nombre=data['nombre'], password=data['password'], fecha_suscripcion=data['fecha_suscripcion'], apellido=data['apellido'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201

# Ruta para actualizar un usuario existente
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.get_json()
        user.nombre = data['nombre']
        user.password = data['password']
        user.fecha_suscripcion = data['fecha_suscripcion']
        user.apellido = data['apellido']
        user.email = data['email']
        db.session.commit()
        return jsonify(user.serialize()), 200
    else:
        return jsonify({"message": "User not found"}), 404

# Ruta para eliminar un usuario existente
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200
    else:
        return jsonify({"message": "User not found"}), 404

# Ruta para obtener todos los personajes
@app.route('/personajes', methods=['GET'])
def get_personajes():
    personajes = Personajes.query.all()
    personajes_serialized = [personaje.serialize() for personaje in personajes]
    return jsonify(personajes_serialized), 200

# Ruta para obtener un personaje por ID
@app.route('/personajes/<int:personaje_id>', methods=['GET'])
def get_personaje(personaje_id):
    personaje = Personajes.query.get(personaje_id)
    if personaje:
        return jsonify(personaje.serialize()), 200
    else:
        return jsonify({"message": "Personaje not found"}), 404

# Ruta para crear un nuevo personaje
@app.route('/personajes', methods=['POST'])
def create_personaje():
    data = request.get_json()
    personaje = Personajes(nombre=data['nombre'], altura=data['altura'], genero=data['genero'], peso=data['peso'])
    db.session.add(personaje)
    db.session.commit()
    return jsonify(personaje.serialize()), 201

# Ruta para actualizar un personaje existente
@app.route('/personajes/<int:personaje_id>', methods=['PUT'])
def update_personaje(personaje_id):
    personaje = Personajes.query.get(personaje_id)
    if personaje:
        data = request.get_json()
        personaje.nombre = data['nombre']
        personaje.altura = data['altura']
        personaje.altura = data['altura']
        personaje.genero = data['genero']
        personaje.peso = data['peso']
        db.session.commit()
        return jsonify(personaje.serialize()), 200
    else:
        return jsonify({"message": "Personaje not found"}), 404

# Ruta para eliminar un personaje existente
@app.route('/personajes/<int:personaje_id>', methods=['DELETE'])
def delete_personaje(personaje_id):
    personaje = Personajes.query.get(personaje_id)
    if personaje:
        db.session.delete(personaje)
        db.session.commit()
        return jsonify({"message": "Personaje deleted"}), 200
    else:
        return jsonify({"message": "Personaje not found"}), 404

# Ruta para obtener todos los planetas
@app.route('/planetas', methods=['GET'])
def get_planetas():
    planetas = Planetas.query.all()
    planetas_serialized = [planeta.serialize() for planeta in planetas]
    return jsonify(planetas_serialized), 200

# Ruta para obtener un planeta por ID
@app.route('/planetas/<int:planeta_id>', methods=['GET'])
def get_planeta(planeta_id):
    planeta = Planetas.query.get(planeta_id)
    if planeta:
        return jsonify(planeta.serialize()), 200
    else:
        return jsonify({"message": "Planeta not found"}), 404

# Ruta para crear un nuevo planeta
@app.route('/planetas', methods=['POST'])
def create_planeta():
    data = request.get_json()
    planeta = Planetas(nombre=data['nombre'], diametro=data['diametro'], periodo_orbital=data['periodo_orbital'], poblacion=data['poblacion'])
    db.session.add(planeta)
    db.session.commit()
    return jsonify(planeta.serialize()), 201

# Ruta para actualizar un planeta existente
@app.route('/planetas/<int:planeta_id>', methods=['PUT'])
def update_planeta(planeta_id):
    planeta = Planetas.query.get(planeta_id)
    if planeta:
        data = request.get_json()
        planeta.nombre = data['nombre']
        planeta.diametro = data['diametro']
        planeta.periodo_orbital = data['periodo_orbital']
        planeta.poblacion = data['poblacion']
        db.session.commit()
        return jsonify(planeta.serialize()), 200
    else:
        return jsonify({"message": "Planeta not found"}), 404

# Ruta para eliminar un planeta existente
@app.route('/planetas/<int:planeta_id>', methods=['DELETE'])
def delete_planeta(planeta_id):
    planeta = Planetas.query.get(planeta_id)
    if planeta:
        db.session.delete(planeta)
        db.session.commit()
        return jsonify({"message": "Planeta deleted"}), 200
    else:
        return jsonify({"message": "Planeta not found"}), 404
    

                #FAVORITOS
    
# Ruta para obtener todos los favoritos de un usuario por ID
@app.route('/users/<int:user_id>/favoritos', methods=['GET'])
def get_user_favoritos(user_id):
    user = User.query.get(user_id)
    if user:
        favoritos = user.favoritos
        favoritos_serialized = [favorito.serialize() for favorito in favoritos]
        return jsonify(favoritos_serialized), 200
    else:
        return jsonify({"message": "User not found"}), 404

# Ruta para agregar un favorito a un usuario
@app.route('/users/<int:user_id>/favoritos', methods=['POST'])
def add_user_favorito(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.get_json()
        favorito = Favoritos(
            usuario_id=user.id,
            personajes_id=data.get('personajes_id'),
            planetas_id=data.get('planetas_id')
        )
        db.session.add(favorito)
        db.session.commit()
        return jsonify(favorito.serialize()), 201
    else:
        return jsonify({"message": "User not found"}), 404

# Ruta para eliminar un favorito de un usuario
@app.route('/users/<int:user_id>/favoritos/<int:favorito_id>', methods=['DELETE'])
def delete_user_favorito(user_id, favorito_id):
    favorito = Favoritos.query.get(favorito_id)
    if favorito:
        db.session.delete(favorito)
        db.session.commit()
        return jsonify({"message": "Favorito deleted"}), 200
    else:
        return jsonify({"message": "Favorito not found"}), 404
    
    
    
    # Ruta para obtener todos los favoritos de un planeta por ID
@app.route('/planetas/<int:planeta_id>/favoritos', methods=['GET'])
def get_planeta_favoritos(planeta_id):
    planeta = Planetas.query.get(planeta_id)
    if planeta:
        favoritos = Favoritos.query.filter_by(planetas_id=planeta_id).all()
        favoritos_serialized = [favorito.serialize() for favorito in favoritos]
        return jsonify(favoritos_serialized), 200
    else:
        return jsonify({"message": "Planeta not found"}), 404

# Ruta para agregar un favorito a un planeta
@app.route('/planetas/<int:planeta_id>/favoritos', methods=['POST'])
def add_planeta_favorito(planeta_id):
    planeta = Planetas.query.get(planeta_id)
    if planeta:
        data = request.get_json()
        favorito = Favoritos(
            planetas_id=planeta_id,
            usuario_id=data.get('usuario_id'),
            personajes_id=data.get('personajes_id')
        )
        db.session.add(favorito)
        db.session.commit()
        return jsonify(favorito.serialize()), 201
    else:
        return jsonify({"message": "Planeta not found"}), 404
    
   # Ruta para renderizar el formulario de registro
@app.route('/signup')
def signup():
    return render_template('signup.html')

# Ruta para renderizar el formulario de inicio de sesión
@app.route('/login')
def login():
    return render_template('login.html')

# Ruta para autenticar y obtener un token de acceso
@app.route('/auth/login', methods=['POST'])
def auth_login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Aquí deberías verificar las credenciales del usuario
    # Si las credenciales son válidas, puedes crear un token de acceso
    if username == 'usuario' and password == 'contraseña':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    return jsonify({'message': 'Credenciales inválidas'}), 401

# Ruta protegida que requiere autenticación
@app.route('/private')
@jwt_required()
def private():
    current_user = get_jwt_identity()
    return render_template('private.html', username=current_user)
    

    
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
