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
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('mohamed','1234','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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
    def test_get_gategories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code , 200)
        self.assertEqual(data['success'] ,True )
        self.assertNotEqual(data['categories'] , None) 

    def test_non_existing_categories(self):
        res = self.client().get('/categories/450')
        data = json.loads(res.data) 
        self.assertEqual(res.status_code , 404)
        self.assertEqual(data['success'] , False) 
        self.assertEqual(data['message'] , 'resource not found')
         

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code , 200)
        self.assertEqual(data['success'] , True)
        self.assertNotEqual(data['questions'] , None)

    def test_non_existing_page_questions(self):
        res = self.client().get('/questions?page=500')
        data = json.loads(res.data) 
        self.assertEqual(res.status_code , 404)
        self.assertEqual(data['success'] , False)
        self.assertEqual(data['message'] , 'resource not found') 

    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True) 


    def test_deleting_non_existing_question(self):
        res = self.client().delete('/questions/444')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable') 

    def test_add_question(self):
        new_question = {'question': 'new TRY','answer': 'new TRY','difficulty': 1,'category': 1}
        old_questions = len(Question.query.all())
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        new_questions = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(new_questions, old_questions + 1) 

    def test_search_for_question(self):
        search_for = {'searchTerm' : 'title'}
        res = self.client().post('/questions/search' , json=search_for)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])

    def test_get_questions_per_category(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])    
    
    def test_play(self):
        new_game = {'previous_questions': 'what does gg mean?','quiz_category': {'id':6 , 'type':'Sports'}}

        res = self.client().post('/quizzes', json=new_game)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


            


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()