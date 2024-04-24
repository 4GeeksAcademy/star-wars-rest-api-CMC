# import os
# import sys
# from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
# from sqlalchemy.orm import relationship, declarative_base
# from sqlalchemy import create_engine
# from eralchemy2 import render_er
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Planets(db.Model):
    __tablename__ = 'planets'
    # Here we define db.Columns for the table person
    # Notice that each db.Column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer)
    averageTemp = db.Column(db.Integer)
    favourites = db.relationship('Favourites', backref='planets', lazy=True)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "average temp": self.averageTemp
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    race = db.Column(db.String(250), nullable=False)
    homeworld = db.Column(db.String(250), nullable=False)
    favourites = db.relationship('Favourites', backref='characters', lazy=True)
    
    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "race": self.race,
            "homeworld": self.homeworld
        }

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    length = db.Column(db.Integer)
    crewSize = db.Column(db.Integer)
    favourites = db.relationship('Favourites', backref='vehicles', lazy=True)

    def __repr__(self):
        return '<Vehicles %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "length (metres)": self.length,
            "crew size": self.crewSize
        }



class Favourites(db.Model):
    __tablename__ = 'favourites'
    id = db.Column(db.Integer, primary_key=True)
    favouritePlanets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    favouriteCharacters_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    favouriteVehicles_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    def __repr__(self):
        return '<Favourites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            # "planet": self.planets_id,
            # "character": self.characters_id,
            # "vehicle": self.vehicles_id
        }


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(411), nullable=False)
    password = db.Column(db.String(16), nullable=False)
    onlinestatus = db.Column(db.Boolean()) 
    favourites = db.relationship('Favourites', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.userName

    def serialize(self):
        return {
            "id": self.id,
            "user name": self.userName,
            "email": self.email,
            "online status": self.onlinestatus,
            # "favourites": self.favourites -- ask about this --
            # do not serialize the password, its a security breach
        }

