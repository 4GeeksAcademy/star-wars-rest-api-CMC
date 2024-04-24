"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Characters, Vehicles, Favourites
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

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# CHARACTERS CHARACTERS CHARACTERS CHARACTERS CHARACTERS CHARACTERS CHARACTERS
# Endpoint to get all characters
@app.route('/characters', methods=['GET'])
def get_all_characters():
    query_results = Characters.query.all()
    results = list(map(lambda item: item.serialize(),query_results))

    if results == []:
        return jsonify({"msg": "No characters found"}), 404
    response_body = {
        "msg": "All ok",
        "results": results
    }

    return jsonify(response_body), 200

# Endpoint to get individual characters
@app.route('/characters/<int:characters_id>', methods=['GET'])
def get_one_character(characters_id):
    query_result = Characters.query.filter_by(id=characters_id).first()
    if query_result is None:
        return jsonify({"msg":"No character with that ID exists"}), 404
    response_body = {
        "msg": "All working",
        "query result": query_result.serialize()
    }

    return jsonify(response_body), 200

# Endpoint for POST for characters
@app.route('/characters', methods=['POST'])
def create_character():
    # query_result = Characters.query.filter_by(id=characters_id).first()
    data = request.json
    print(data)
    new_character = Characters(name=data["name"], race=data["race"], homeworld=data["homeworld"])
    print(new_character)
    db.session.add(new_character)
    db.session.commit()
    response_body = {
        "msg": "All working",
        # "query result": query_result
    }

    return jsonify(response_body), 200

# Endpoint for Add a new favourite character to the current user with the character id = character_id.
# @app.route('/favourites/characters/<int:characters_id>', methods=['POST'])
# def create_character_in_favourites(characters_id):
#     # query_result = Characters.query.filter_by(id=characters_id).first()
#     data = request.json
#     print(data)
#     new_character = Characters(name=data["name"], race=data["race"], homeworld=data["homeworld"])
#     print(new_character)
#     db.session.add(new_character)
#     db.session.commit()
#     response_body = {
#         "msg": "Character successfully added to favourites",
#         # "query result": query_result
#     }

#     return jsonify(response_body), 200

@app.route('/favourites/characters/<int:characters_id>', methods=['POST'])
def create_character_in_favourites(characters_id):
    data = request.json
    print(data)
    print(characters_id)
    user_exists = User.query.filter_by(id=data["user_id"]).first()
    characters_exists = Characters.query.filter_by(id=characters_id).first()
    
    if user_exists and characters_exists: 


        query_results = Favourites.query.filter_by(favouriteCharacters_id=characters_id, user_id=data["user_id"]).first()

        if query_results is None: 

            new_favorite = Favourites(favouriteCharacters_id=characters_id, user_id=data["user_id"])
            db.session.add(new_favorite)
            db.session.commit()
            return ({"msg": "ok"}), 200     

        else:
            return ({"msg": "this user already has this character as a favorite"}), 200
        
    elif user_exists is None and characters_exists is None:
        return ({"msg": "both user and character do not exist"}), 400
    
    elif user_exists is None: 
        return ({"msg": "this user does not exist"}), 400
    
    elif characters_exists is None: 
        return ({"msg": "this character does not exist"}), 400 
    
# Endpoint for deleting a favourite character of the current user
@app.route('/favourites/characters/<int:characters_id>', methods=['DELETE'])
def delete_one_favourite_character(characters_id):
    data = request.json
    
    user_id = data["user_id"]
    character_to_delete = Favourites.query.filter_by(favouriteCharacters_id=characters_id, user_id=user_id).first()
    print(character_to_delete)

    if character_to_delete:
        db.session.delete(character_to_delete)
        db.session.commit()
        print(f"User with ID {user_id} deleted successfully.")

        response_body = {
        "msg": "Successfully deleted from favourites"
        }
        return jsonify(response_body), 200
    else:
        return(f"User with ID {user_id} not found."), 404

# PLANETS PLANETS PLANETS PLANETS PLANETS PLANETS PLANETS PLANETS PLANETS PLANETS PLANETS
# Endpoint to get all planets
@app.route('/planets', methods=['GET'])
def get_all_planets():
    query_results = Planets.query.all()
    results = list(map(lambda item: item.serialize(),query_results))

    if results == []:
        return jsonify({"msg": "No planets found"}), 404
    response_body = {
        "msg": "All ok",
        "results": results
    }

    return jsonify(response_body), 200

# Endpoint to get individual planets
@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_one_planet(planets_id):
    query_result = Planets.query.filter_by(id=planets_id).first()
    if query_result is None:
        return jsonify({"msg": "no planet with that ID"}), 404
    response_body = {
        "msg": "ok",
        "result":query_result.serialize()
    }

    return jsonify(response_body), 200

# Endpoint to add a new planet to planet list with the planet id = planet_id.
@app.route('/planets', methods=['POST'])
def create_planet():
    # query_result = Characters.query.filter_by(id=characters_id).first()
    data = request.json
    print(data)
    new_planet = Planets(name=data["name"], population=data["population"], averageTemp=data["averageTemp"])
    print(new_planet)
    db.session.add(new_planet)
    db.session.commit()
    response_body = {
        "msg": "Planet has been successfully added",
        "new planet": new_planet
    }

    return jsonify(response_body), 200

# Endpoint for adding a new favourite planet to the current user
@app.route('/favourites/planets/<int:planets_id>', methods=['POST'])
def create_planet_in_favourites(planets_id):
    data = request.json
    print(data)
    print(planets_id)
    user_exists = User.query.filter_by(id=data["user_id"]).first()
    planets_exists = Planets.query.filter_by(id=planets_id).first()
    
    if user_exists and planets_exists: 


        query_results = Favourites.query.filter_by(favouritePlanets_id=planets_id, user_id=data["user_id"]).first()

        if query_results is None: 

            new_favorite = Favourites(favouritePlanets_id=planets_id, user_id=data["user_id"])
            db.session.add(new_favorite)
            db.session.commit()
            return ({"msg": "ok"}), 200

       

        else:
            return ({"msg": "this user already has this planet as a favorite"}), 200
        
    elif user_exists is None and planets_exists is None:
        return ({"msg": "both user and planet do not exist"}), 400
    
    elif user_exists is None: 
        return ({"msg": "this user does not exist"}), 400
    
    elif planets_exists is None: 
        return ({"msg": "this planet does not exist"}), 400 

# Endpoint for deleting a favourite planet of the current user
@app.route('/favourites/planets/<int:planets_id>', methods=['DELETE'])
def delete_one_favourite_planet(planets_id):
    data = request.json
    
    user_id = data["user_id"]
    planet_to_delete = Favourites.query.filter_by(favouritePlanets_id=planets_id, user_id=user_id).first()
    print(planet_to_delete)

    if planet_to_delete:
        db.session.delete(planet_to_delete)
        db.session.commit()
        print(f"User with ID {user_id} deleted successfully.")

        response_body = {
        "msg": "Successfully deleted from favourites"
        }
        return jsonify(response_body), 200
    else:
        return(f"User with ID {user_id} not found."), 404


# VEHICLES VEHICLES VEHICLES VEHICLES VEHICLES VEHICLES VEHICLES VEHICLES VEHICLES VEHICLES
# Endpoint to get all vehicles
@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    query_results = Vehicles.query.all()
    results = list(map(lambda item: item.serialize(),query_results))
   
    if results == []:
        return jsonify({"msg": "No vehicles found"}), 404
    response_body = {
        "msg": "All ok",
        "results": results
    }

    return jsonify(response_body), 200

# Endpoint to get a specific vehicle
@app.route('/vehicles/<int:vehicles_id>', methods=['GET'])
def get_one_vehicle(vehicles_id):
    query_result = Vehicles.query.filter_by(id=vehicles_id).first()
    print(query_result.serialize())
    response_body = {
        "msg": "All working",
        "query result": query_result.serialize()
    }

    return jsonify(response_body), 200

# Endpoint for Add a new favourite vehicle to the current user with the vehicles id = vehicles_id.
@app.route('/favourites/vehicles/<int:vehicles_id>', methods=['POST'])
def create_vehicle_in_favourites(vehicles_id):
    data = request.json
    print(data)
    print(vehicles_id)
    user_exists = User.query.filter_by(id=data["user_id"]).first()
    vehicles_exists = Vehicles.query.filter_by(id=vehicles_id).first()
    
    if user_exists and vehicles_exists: 


        query_results = Favourites.query.filter_by(favouritePlanets_id=vehicles_id, user_id=data["user_id"]).first()

        if query_results is None: 

            new_favorite = Favourites(favouritePlanets_id=vehicles_id, user_id=data["user_id"])
            db.session.add(new_favorite)
            db.session.commit()
            return ({"msg": "ok"}), 200

       

        else:
            return ({"msg": "this user already has this vehicles as a favorite"}), 200
        
    elif user_exists is None and vehicles_exists is None:
        return ({"msg": "both user and vehicles do not exist"}), 400
    
    elif user_exists is None: 
        return ({"msg": "this user does not exist"}), 400
    
    elif vehicles_exists is None: 
        return ({"msg": "this vehicles does not exist"}), 400
    
# Endpoint for deleting a favourite vehicle of the current user
@app.route('/favourites/vehicles/<int:vehicles_id>', methods=['DELETE'])
def delete_one_favourite_vehicle(vehicles_id):
    data = request.json
    
    user_id = data["user_id"]
    vehicle_to_delete = Favourites.query.filter_by(favouriteVehicles_id=vehicles_id, user_id=user_id).first()
    print(vehicle_to_delete)

    if vehicle_to_delete:
        db.session.delete(vehicle_to_delete)
        db.session.commit()
        print(f"User with ID {user_id} deleted successfully.")

        response_body = {
        "msg": "Successfully deleted from favourites"
        }
        return jsonify(response_body), 200
    else:
        return(f"User with ID {user_id} not found."), 404

# USERS USERS USERS USERS USERS USERS USERS USERS USERS USERS USERS USERS USERS
# Endpoint to get all users
@app.route('/user', methods=['GET'])
def get_all_users():
    query_results = User.query.all()
    results = list(map(lambda item: item.serialize(),query_results))

    if results == []:
        return jsonify({"msg": "No users found"}), 404
    response_body = {
        "msg": "All ok",
        "results": results
    }

    return jsonify(response_body), 200


# Endpoint to get specific user
@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    query_result = User.query.filter_by(id=user_id).first()
    if query_result is None:
        return jsonify({"msg": "no user with ID provided"}), 404
    response_body = {
        "msg": "It's working, all ok",
        "query result": query_result.serialize()
    }

    return jsonify(response_body), 200

# Endpoint for POST for users
@app.route('/users', methods=['POST'])
def create_user():
    # query_result = Characters.query.filter_by(id=characters_id).first()
    data = request.json
    print(data)
    new_user = User(user_name=data["user_name"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    response_body = {
        "msg": "All working",
        # "query result": query_result
    }

    return jsonify(response_body), 200

# FAVOURITES FAVOURITES FAVOURITES FAVOURITES FAVOURITES FAVOURITES FAVOURITES FAVOURITES FAVOURITES
# Endpoint to get all favourites of a user
@app.route('/users/favourites', methods=['GET'])
def get_all_user_favourites():
    query_results = Favourites.query.all()
    results = list(map(lambda item: item.serialize(),query_results))

    if results == []:
        return jsonify({"msg": "No users found"}), 404
    response_body = {
        "msg": "All ok",
        "results": results
    }

    return jsonify(response_body), 200

@app.route('/users/favourites/<int:user_id>', methods=['GET'])
def get_all_favourites(user_id):
    query_results = Favourites.query.filter_by(user_id=user_id).first()
    print(query_results)
    
    if query_results is None:
        return jsonify({"msg": "No matching user with that ID"}), 404
    response_body = {
        "msg": "All ok",
        "results": query_results.serialize()
    }

    return jsonify(response_body), 200

# JWT JWT JWT JWT JWT JWT JWT JWT JWT JWT JWT JWT JWT JWT JWT JWT JWT JWT JWT JWT JWT JWT
# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    new_signup = User(userName=data.get("userName"), email=data.get("email"), password=data.get("password"))
    db.session.add(new_signup)
    db.session.commit()
    return jsonify({"msg": "User signed up successfully"}), 200


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    userName = data.get("userName", None)
    password = data.get("password", None)
    
    username_result = User.query.filter_by(userName=userName).first()
    
    print(userName)
    print(password)
    print(username_result.userName)
    print(username_result.password)
    # if userName is None or password is None:
    #     return jsonify({"msg": "Bad username or password"}), 404
    if userName != username_result.userName or password != username_result.password:
        return jsonify({"msg": "Bad username or password"}), 401

    # return jsonify({"msg": "User logged in successfully"}), 200
    access_token = create_access_token(identity=userName)
    return jsonify(access_token=access_token), 200


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/private", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# validToken: function () {
# 				fetch(`https://humble-space-orbit-4jjwqw7xr9w4f7j6w-3000.app.github.dev/valid-token`, {
# 					method: 'GET',
# 					headers: {
# 						'Content-Type': 'application/json',
# 						'Authorization': 'Bearer ' + localStorage.getItem("access_token")
# 					}
# 				})
# 					.then(res => {
# 						res.json()
# 						if (res.status == 200) { setStore({ validacion: true }) };
# 					})
# 					.then(data => {
# 						console.log(data);
# 					})
# 					.catch(err => console.error(err))
# 			}

@app.route("/valid-token", methods=["GET"])
@jwt_required()
def valid_token():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    consulta = User.query.filter_by(email=current_user).first()


    if consulta is None :
        return jsonify({"msg":"el usuario no existe", "estado":False}, 404)
    

    return jsonify({"estado":True}), 200

# @app.route('/characters', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /characters response "
#     }

#     return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
