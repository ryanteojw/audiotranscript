import unittest
from app import app, db

class SetUpTestCase(unittest.TestCase):
    # setup the flask app
    def setUp(self):
        self.client = app.test_client()
    # close all connections
    def tearDown(self):
        print("Running tearDown!")
        with app.app_context():
            db.session.remove()
            db.session.close()
            db.engine.dispose()
