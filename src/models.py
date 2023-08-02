from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    fecha_suscripcion =  db.Column(db.String(50), nullable=True)
    apellido =  db.Column(db.String(250), nullable=False)
    email =  db.Column(db.String(250), unique=True, nullable=False)
    favoritos = db.relationship('Favoritos',backref='user', lazy=True)
    
    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "fecha_suscripcion": self.fecha_suscripcion,
            "apellido": self.apellido,
            #"favoritos": self.favoritos,
            # do not serialize the password, its a security breach
        }
        
class Personajes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    altura = db.Column(db.String(250), nullable=False)
    genero =  db.Column(db.String(250), nullable=False)
    peso =  db.Column(db.String(250), nullable=False)
    favoritos = db.relationship('Favoritos',backref='personajes', lazy=True)        
    
    def __repr__(self):
        return '<Personajes %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "altura": self.altura,
            "genero": self.genero,
            "peso": self.peso,
            #"favoritos": self.favoritos,
            # do not serialize the password, its a security breach
        }
        
class Planetas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    diametro = db.Column(db.String(250), nullable=False)
    periodo_orbital =  db.Column(db.String(250), nullable=False)
    poblacion =  db.Column(db.String(250), nullable=False)
    favoritos = db.relationship('Favoritos',backref='planetas', lazy=True)  
    
    def __repr__(self):
        return '<Planetas %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "diametro": self.diametro,
            #"favoritos": self.favoritos,
            "periodo_orbital": self.periodo_orbital,
            # do not serialize the password, its a security breach          
            }
        
class Favoritos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planetas_id = db.Column(db.Integer, db.ForeignKey('planetas.id'))
    personajes_id = db.Column(db.Integer, db.ForeignKey('personajes.id'))
    
    def __repr__(self):
        return '<Favoritos %r>' % self.id

    def serialize(self):
        query_planeta = Planetas.query.filter_by(id=self.planetas_id).first()
        query_personaje = Personajes.query.filter_by(id=self.personajes_id).first()
        result_planeta = None
        result_personaje = None
        if query_planeta is None : 
            result_planeta 
        else :
            result_planeta = query_planeta.serialize()
            
        if query_personaje is None : 
            result_personaje 
        else :
            result_personaje = query_personaje.serialize()
            
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "planetas_id": self.planetas_id,
            "personajes_id": self.personajes_id,
            "info_planeta": result_planeta,
            "info_personajes": result_personaje,
            # do not serialize the password, its a security breach          
            }
            