import unittest
from unittest.mock import patch
from mongomock import MongoClient
from src import create_app
import src.database

class PyMongoMock(MongoClient):
    def init_app(self, app):
        return super().__init__()

class TestUsersRegistration(unittest.TestCase):
    def test_inscription(self):
        request = {
            "username": "demo",
            "password": "demo",
            "email": "demo@gmail.com"
        }

        with patch.object(src.database, "mongo", PyMongoMock()):
            app = create_app("mongodb://localhost:27017/db").test_client()
            response = app.post("/register", json=request)
            self.assertEqual(response.status_code, 200)

            # Validate the content
            response_json = response.get_json()
            expected_json = {
                "status": 200,
                "msg": "Registration successful, please check your mail to confirm your account",
            }
            self.assertEqual(response_json, expected_json)

    def test_inscription(self):
        request = {
            "username": "demo",
            "password": "demo",
            "email": "demo@gmail.com"
        }

        with patch.object(src.database, "mongo", PyMongoMock()):
            app = create_app("mongodb://localhost:27017/db").test_client()
            response = app.post("/register", json=request)
            self.assertEqual(response.status_code, 200)

            # Validate the content
            response_json = response.get_json()
            expected_json = {
                "status": 200,
                "msg": "Registration successful, please check your mail to confirm your account",
            }
            self.assertEqual(response_json, expected_json)