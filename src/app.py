"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personajes, Planetas, Favoritos
#from models import Person
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

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
#Configure la extensión Flask-JWT-Extended
app.config["JWT_SECRET_KEY"] = "4geeks"  
jwt = JWTManager(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# obtiene los datos de todos los usuarios
@app.route('/user', methods=['GET'])
def handle_hello():
    #querys o consultas
    users_query = User.query.all()
    result = list(map(lambda item: item.serialize(),users_query))
    
    response_body = {
        "msg": "ok",
        "results": result
    }

    return jsonify(response_body), 200

# obtiene los datos de un usuario
@app.route('/user/<int:user_id>', methods=['GET'])
def get_info_user(user_id):
    user_query = User.query.filter_by(id=user_id).first()
#querys o consultas
    response_body = {
        "msg": "ok",
        "result": user_query.serialize()
    }
    
    return jsonify(response_body), 200

# crea un usuario nuevo 
@app.route('/user', methods=['POST'])
def create_user():
    request_body = request.json
    user_query = User.query.filter_by(email=request_body["email"]).first()

    if user_query is None:
        user = User(email=request_body["email"], password=request_body["password"], nombre=request_body["nombre"], apellido=request_body["apellido"], fecha_suscripcion=request_body["fecha_suscripcion"])
        
        db.session.add(user)
        db.session.commit()
        
        response_body = {
            "msg": "El usuario ha sido creado con exito",
        }
        return jsonify(response_body), 200
    else:
        return jsonify({"msg":"Usuario ya existe"}), 400

# obtiene los datos de todos los personajes
@app.route('/personajes', methods=['GET'])
def load_personajes():
    personajes_query = Personajes.query.all()
    results = list(map(lambda item: item.serialize(),personajes_query))
    ##querys o consultas
    response_body = {
        "msg": "ok",
        "results": results
    }

    return jsonify(response_body), 200

# obtiene los datos de un personaje
@app.route('/personajes/<int:personaje_id>', methods=['GET'])
def get_info_personajes(personaje_id):
    personajes_query = Personajes.query.filter_by(id=personaje_id).first()
##querys o consultas
    response_body = {
        "msg": "ok",
        "result": personajes_query.serialize()
    }

    return jsonify(response_body), 200

# obtiene los datos de todos los planetas
@app.route('/planetas', methods=['GET'])
def load_planetas():
    planetas_query = Planetas.query.all()
    results = list(map(lambda item: item.serialize(),planetas_query))
    response_body = {
        "msg": "ok",
        "results": results
    }

    return jsonify(response_body), 200

# obtiene los datos de un planeta
@app.route('/planetas/<int:planeta_id>', methods=['GET'])
def get_info_planetas(planeta_id):
    planetas_query = Planetas.query.filter_by(id=planeta_id).first()
##querys o consultas
    response_body = {
        "msg": "ok",
        "result": planetas_query.serialize()
    }

    return jsonify(response_body), 200

# obtiene los datos de todos los favoritos
@app.route('/favoritos', methods=['GET'])
def load_favoritos():
    favorito_query = Favoritos.query.all() 
    results = list(map(lambda item: item.serialize(),favorito_query))
    
    
    response_body = {
        "msg": "ok",
        "results": results
        }

    return jsonify(response_body), 200

# obtiene los datos favoritos de un usuario
@app.route('/user/<int:usuario_id>/favoritos', methods=['GET'])
def  get_info_favoritos (usuario_id):
    # consulta
    favoritos_query = Favoritos.query.filter_by(usuario_id=usuario_id).all()
    results= list(map(lambda item: item.serialize(),favoritos_query))
    
    response_body = {
        "msj" : "tus favoritos" ,
        "result": results
    }

    return jsonify(response_body), 200


@app.route('/favoritos/planetas/<int:planetas_id>', methods=['POST'])
def create_favorito_planeta(planetas_id):
    request_body = request.json
    planeta_fav = Favoritos(usuario_id=request_body["usuario_id"], planetas_id=planetas_id)
    db.session.add(planeta_fav)
    db.session.commit()
    response_body = {
            "msg": "el planeta favorito fue creado con exito",
        }

    return jsonify(response_body), 200  

@app.route('/favoritos/personajes/<int:personaje_id>', methods=['POST'])
def create_favorito_personaje(personaje_id):
    request_body = request.json
    personaje_fav = Favoritos(usuario_id=request_body["usuario_id"], personajes_id=personaje_id)
    db.session.add(personaje_fav)
    db.session.commit()
    response_body = {
            "msg": "el planeta favorito fue creado con exito",
        }

    return jsonify(response_body), 200 

# eliminar un planeta faorito de un usuario 
@app.route('/favoritos/planetas/<int:position>', methods=['DELETE'])
def delete_favorito_planeta(position):
    request_body = request.json
    planetas_query = Favoritos.query.filter_by(usuario_id=request_body["usuario_id"], planetas_id=position).first()
    if planetas_query is None : 
        response_body = {
            "msg": "el planeta no existe",
        }
        return  jsonify(response_body), 200
    else :
        db.session.delete(planetas_query)
        db.session.commit()
        response_body = {
                "msg": "el planeta fue eliminado con exito",
                "result": planetas_query.serialize()
            }
        return  jsonify(response_body), 200

# eliminar un personaje faorito de un usuario 
@app.route('/favoritos/personajes/<int:position>', methods=['DELETE'])
def delete_favorito_personaje(position):
    request_body = request.json
    personaje_query = Favoritos.query.filter_by(usuario_id=request_body["usuario_id"], personajes_id=position).first()
    if personaje_query is None : 
        response_body = {
            "msg": "el personaje no existe",
        }
        return  jsonify(response_body), 200
    else :
        db.session.delete(personaje_query)
        db.session.commit()
        response_body = {
                "msg": "el personaje fue eliminado con exito",
                "result": personaje_query.serialize()
            }
        return  jsonify(response_body), 200

# crea un nuevo planeta  
@app.route('/planetas', methods=['POST'])
def create_planeta():
    request_body = request.json
    
    planeta = Planetas(nombre=request_body["nombre"], diametro=request_body["diametro"], periodo_orbital=request_body["periodo_orbital"], poblacion=request_body["poblacion"])
    
    db.session.add(planeta)
    db.session.commit()
    response_body = {
            "msg": "el planeta fue creado con exito",
        }

    return jsonify(response_body), 200  
  
# crea un nuevo personaje 
@app.route('/personajes', methods=['POST'])
def create_personaje ():
    request_body = request.json
    nombre= request_body["nombre"]
    personaje  = Personajes(nombre=request_body["nombre"], altura=request_body["altura"], genero=request_body["genero"], peso=request_body["peso"])
    
    db.session.add(personaje)
    db.session.commit()
    response_body = {
            "msg": "el personaje " + nombre +" fue creado con exito",
        }

    return jsonify(response_body), 200 
    
#borrar un planeta
@app.route('/planetas/<int:position>', methods=['DELETE'])
def delete_planetas(position):
    planetas_query = Planetas.query.filter_by(id=position).first()
    if planetas_query is None : 
        response_body = {
            "msg": "el planeta no existe",
        }
        return  jsonify(response_body), 200
    else :
        db.session.delete(planetas_query)
        db.session.commit()
        
        response_body = {
                "msg": "el planeta fue eliminado con exito",
                "result": planetas_query.serialize()
            }
        return  jsonify(response_body), 200

#borrar un personaje
@app.route('/personajes/<int:position>', methods=['DELETE'])
def delete_personajes(position):
    personajes_query = Personajes.query.filter_by(id=position).first()
    if personajes_query is None : 
        response_body = {
            "msg": "el planeta no existe",
        }
        return  jsonify(response_body), 200
    else :
        db.session.delete(personajes_query)
        db.session.commit()
        
        response_body = {
                "msg": "el personaje fue eliminado con exito",
                "result": personajes_query.serialize()
            }
        return  jsonify(response_body), 200


    
# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    # request_body = request.json
    # request_body = request.get_json()
    email = request.json.get("email", None)
    password = request.json.get("password", None)
# hacemos una consulta a la tabla para saber si el user existe
    user = User.query.filter_by(email=email).first()
#si no existe devuelvo msg
    if user is None:
        return jsonify({"msg": "User dosn´t exist"}), 404
    
    if email != user.email or password != user.password:
        return jsonify({"msg": "Bad email or password"}), 401
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

#crear nuevo usaurio 
@app.route("/signup", methods=["POST"])
def singup():
    request_body = request.json
    user_query = User.query.filter_by(email=request_body["email"]).first()

    if user_query is None:
        user = User(email=request_body["email"], password=request_body["password"], nombre=request_body["nombre"], apellido=request_body["apellido"], fecha_suscripcion=request_body["fecha_suscripcion"])
        db.session.add(user)
        db.session.commit()
        
        response_body = {
            "msg": "El usuario ha sido creado con exito",
        }
        return jsonify(response_body), 200
    else:
        return jsonify({"msg":"Usuario ya existe"}), 400
    


@app.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    # Accede a la identidad del usuario actual con get_jwt_identity
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    if user != None:
        
        return jsonify({"isLogged":True}), 200
    else:
        return jsonify({"isLogged":False}), 401
    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)