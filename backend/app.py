import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flask_migrate import Migrate
from models import setup_db, db_drop_and_create_all, Actor, Movie, db
from auth import AuthError, requires_auth

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    migrate = Migrate(app, db)  # ✅ Flask-Migrate integration
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PATCH,DELETE,OPTIONS')
        return response

    # ROUTES

    # GET /actors
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        return jsonify({"success": True,
                        "actors": [actor.format() for actor in actors]}), 200

    # GET /movies
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        return jsonify({"success": True,
                        "movies": [movie.format() for movie in movies]}), 200

    # POST /actors
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        data = request.get_json()
        if not data:
            abort(400, "Request body is empty")
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        if not name or not age or not gender:
            abort(422, "Missing actor fields")

        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()
        return jsonify({"success": True, "actor": actor.format()}), 201

    # POST /movies
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        data = request.get_json()
        if not data:
            abort(400, "Request body is empty")
        title = data.get('title')
        release_date = data.get('release_date')
        if not title or not release_date:
            abort(422, "Missing movie fields")

        movie = Movie(title=title, release_date=release_date)
        movie.insert()
        return jsonify({"success": True, "movie": movie.format()}), 201

    # PATCH /actors/<id>
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404, "Actor not found")

        data = request.get_json()
        if 'name' in data:
            actor.name = data['name']
        if 'age' in data:
            actor.age = data['age']
        if 'gender' in data:
            actor.gender = data['gender']

        actor.update()
        return jsonify({"success": True, "actor": actor.format()}), 200

    # PATCH /movies/<id>
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404, "Movie not found")

        data = request.get_json()
        if 'title' in data:
            movie.title = data['title']
        if 'release_date' in data:
            movie.release_date = data['release_date']

        movie.update()
        return jsonify({"success": True, "movie": movie.format()}), 200

    # DELETE /actors/<id>
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404, "Actor not found")

        actor.delete()
        return jsonify({"success": True, "delete": actor_id}), 200

    # DELETE /movies/<id>
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404, "Movie not found")

        movie.delete()
        return jsonify({"success": True, "delete": movie_id}), 200

    # ✅ MANY-TO-MANY ASSOCIATION ENDPOINTS
    @app.route('/movies/<int:movie_id>/actors', methods=['POST'])
    @requires_auth('patch:movies')
    def add_actor_to_movie(payload, movie_id):
        data = request.get_json()
        if not data or 'actor_id' not in data:
            abort(422, "actor_id required")
        movie = Movie.query.get(movie_id)
        actor = Actor.query.get(data['actor_id'])
        if not movie or not actor:
            abort(404, "Movie or Actor not found")

        if actor not in movie.actors:
            movie.actors.append(actor)
            db.session.commit()
        return jsonify({"success": True, "movie": movie.format()}), 200

    @app.route('/movies/<int:movie_id>/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('patch:movies')
    def remove_actor_from_movie(payload, movie_id, actor_id):
        movie = Movie.query.get(movie_id)
        actor = Actor.query.get(actor_id)
        if not movie or not actor:
            abort(404, "Movie or Actor not found")

        if actor in movie.actors:
            movie.actors.remove(actor)
            db.session.commit()
        return jsonify({"success": True, "movie": movie.format()}), 200

    # ERROR HANDLERS
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": str(error)}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"success": False, "error": 401, "message": "Unauthorized"}), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": str(error)}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False, "error": 422, "message": str(error)}), 422

    @app.errorhandler(AuthError)
    def auth_error(err):
        return jsonify({"success": False,
                        "error": err.status_code,
                        "message": err.error['description']}), err.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
