import os
import unittest
import json
from app import create_app
from models import setup_db, db_drop_and_create_all, Actor, Movie

ASSISTANT = os.environ.get('ASSISTANT_TOKEN','').strip()
DIRECTOR = os.environ.get('DIRECTOR_TOKEN','').strip()
PRODUCER = os.environ.get('PRODUCER_TOKEN','').strip()

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.getenv('TEST_DATABASE_URL', 'postgresql://postgres:sukh123@localhost:5432/casting_agency_test')

        with self.app.app_context():
            db_drop_and_create_all()

    def auth_header(self, token):
        return {'Authorization': f'Bearer {token}'}

   
    def test_get_actors_assistant(self):
        res = self.client().get('/actors', headers=self.auth_header(ASSISTANT))
        self.assertEqual(res.status_code, 200)

    
    def test_get_actors_no_auth(self):
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 401)

    
    def test_post_actor_director(self):
        data = {"name": "John", "age": 30, "gender": "Male"}
        res = self.client().post('/actors', headers=self.auth_header(DIRECTOR), json=data)
        self.assertEqual(res.status_code, 201)

    
    def test_post_actor_missing_fields(self):
        data = {"name": "Incomplete"}
        res = self.client().post('/actors', headers=self.auth_header(DIRECTOR), json=data)
        self.assertEqual(res.status_code, 422)

    
    def test_patch_actor_director(self):
        with self.app.app_context():
            actor = Actor(name="Old", age=50, gender="Male")
            actor.insert()
            actor_id = actor.id
        res = self.client().patch(f'/actors/{actor_id}', headers=self.auth_header(DIRECTOR),
                                  json={"name": "New Name"})
        self.assertEqual(res.status_code, 200)

  
    def test_patch_actor_not_found(self):
        res = self.client().patch('/actors/999', headers=self.auth_header(DIRECTOR), json={"name": "X"})
        self.assertEqual(res.status_code, 404)

    
    def test_delete_actor_director(self):
        with self.app.app_context():
            actor = Actor(name="To Delete", age=40, gender="Female")
            actor.insert()
            actor_id = actor.id
        res = self.client().delete(f'/actors/{actor_id}', headers=self.auth_header(PRODUCER))
        self.assertEqual(res.status_code, 200)

   
    def test_delete_actor_not_found(self):
        res = self.client().delete('/actors/999', headers=self.auth_header(PRODUCER))
        self.assertEqual(res.status_code, 404)

    
    def test_rbac_assistant_cannot_delete_movie(self):
        res = self.client().delete('/movies/1', headers=self.auth_header(ASSISTANT))
        self.assertEqual(res.status_code, 403)

    
    def test_rbac_producer_delete_movie(self):
        with self.app.app_context():
            m = Movie(title="Test", release_date="2024-01-01")
            m.insert()
            movie_id = m.id
        res = self.client().delete(f'/movies/{movie_id}', headers=self.auth_header(PRODUCER))
        self.assertEqual(res.status_code, 200)

  
    def test_post_movie_missing_fields(self):
        data = {"title": "No Date"}
        res = self.client().post('/movies', headers=self.auth_header(PRODUCER), json=data)
        self.assertEqual(res.status_code, 422)

    
    def test_get_movies_assistant(self):
        res = self.client().get('/movies', headers=self.auth_header(ASSISTANT))
        self.assertEqual(res.status_code, 200)

    
    def test_get_movies_no_auth(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)

if __name__ == "__main__":
    unittest.main()
