import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgres://postgres:7996@localhost:5432/trivia_test"
        setup_db(self.app, self.database_path)

        self.question = {
            'question': 'Where is the pyramids?',
            'answer': 'Egypt', 
            'category': 3, 
            'difficulty': 2, 
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_no_questions(self):
        res = self.client().get('/questions?page=77777')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)   

    def test_delete_question(self):
        res = self.client().delete('/questions/14')
        data = json.loads(res.data)
        question= Question.query.get(14)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 14)

    def test_create_new_question(self):
        res =  self.client().post('/questions', json=self.question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_create_with_wrong_url(self):
        res = self.client().post('/questions/7777', json=self.question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
    
    def test_get_empty_search(self):
        res = self.client().post('/questions/search', json={'searchTerm':''})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False) 

    def test_get_category_questions(self):    
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_get_empty_category_questions(self):    
        res = self.client().get('/categories/77/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False) 


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()