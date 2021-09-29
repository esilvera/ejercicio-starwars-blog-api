from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50), default="")
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    favorites_planets = db.relationship('Planet', cascade="all, delete", secondary="favorites_planets") # JOIN SQL MANY TO MANY
    favorites_characters = db.relationship('Character', cascade="all, delete", secondary="favorites_characters") # JOIN SQL MANY TO MANY
    
    #def __repr__(self):
        #return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
    
    def serialize_user_register(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

    def serialize_with_favorites(self):
        return {
            "id": self.id,
            "name": self.name,
            "favorites_planets": self.get_planets(),
            "favorites_characters": self.get_characters()
        }

    def get_planets(self):
        return list(map(lambda planet: planet.serialize(), self.favorites_planets))

    def get_characters(self):
        return list(map(lambda character: character.serialize(), self.favorites_characters))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    hair_color = db.Column(db.String(50), default="")
    eye_color = db.Column(db.String(50), default="")
    gender = db.Column(db.String(50), default="")
    description = db.Column(db.String(250), default="")
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id", ondelete='CASCADE'), nullable=False)
    users = db.relationship('User', cascade="all, delete", secondary="favorites_characters")
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "description": self.description,
            "homeworld": self.planet.name #traemos de la tabla planeta el nombre del planeta
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    diameter = db.Column(db.String(150), default="")
    rotation_period = db.Column(db.String(50), default="")
    population = db.Column(db.String(150), default="")
    climate = db.Column(db.String(150), default="")
    terrain = db.Column(db.String(150), default="")
    characters = db.relationship("Character", cascade="all, delete", backref="planet") # JOIN SQL ONE TO MANY
    #users = db.relationship('User', cascade="all, delete", secondary="favorites_users")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class FavoritePlanet(db.Model):
    __tablename__ = 'favorites_planets'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id', ondelete='CASCADE'), primary_key=True)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "planet_id": self.planet_id
            #"favorite_planet": self.planet.name, #traemos de la tabla Planet el nombre del planeta
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class FavoriteCharacter(db.Model):
    __tablename__ = 'favorites_characters'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id', ondelete='CASCADE'), primary_key=True)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "character_id": self.character_id
            #"favorite_character": self.character.name #traemos de la tabla Character el nombre del Pesonaje
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()