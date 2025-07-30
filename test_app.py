import os
import unittest
import json
from app import create_app
from models import setup_db, db_drop_and_create_all, Actor, Movie

ASSISTANT = os.environ.get('ASSISTANT_TOKEN')
DIRECTOR = os.environ.get('DIRECTOR_TOKEN')
PRODUCER = os.environ.get('PRODUCER_TOKEN')

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

        # ✅ use a dedicated test DB
        self.database_path = os.getenv('TEST_DATABASE_URL', 'postgresql://postgres:sukh123@localhost:5432/casting_agency_test')

        # ✅ drop and recreate tables before each test
        with self.app.app_context():
            db_drop_and_create_all()

    def auth_header(self, token):
        return {'Authorization': f'Bearer {token}'}

    # GET actors (Assistant)
    def test_get_actors_assistant(self):
        res = self.client().get('/actors', headers=self.auth_header(ASSISTANT))
        self.assertEqual(res.status_code, 200)

    # POST actor (Director)
    def test_post_actor_director(self):
        data = {"name": "John", "age": 30, "gender": "Male"}
        res = self.client().post('/actors', headers=self.auth_header(DIRECTOR), json=data)
        self.assertEqual(res.status_code, 201)

    # RBAC: Assistant cannot delete movie
    def test_rbac_assistant_cannot_delete_movie(self):
        res = self.client().delete('/movies/1', headers=self.auth_header(ASSISTANT))
        self.assertEqual(res.status_code, 403)

    # RBAC: Producer can delete movie
    def test_rbac_producer_delete_movie(self):
        with self.app.app_context():
            m = Movie(title="Test", release_date="2024-01-01")
            m.insert()
            movie_id = m.id  # store id while still in context
        res = self.client().delete(f'/movies/{movie_id}', headers=self.auth_header(PRODUCER))
        self.assertEqual(res.status_code, 200)
if __name__ == "__main__":
    unittest.main()

