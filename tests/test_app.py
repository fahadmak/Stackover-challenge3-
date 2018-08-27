import unittest

from flask import json

from app import views, app

from test_data import post_question1, post_question2, post_question3, post_question4, post_question5, post_question6, post_question7, post_question8, post_answer1, post_answer2

class QuestionsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_question_creation(self):
        """Test API can create a question (POST request)"""
        response = self.app.post('api/v1/questions', content_type='application/json',
                                 data=json.dumps(post_question1))
        self.assertEqual(response.status_code, 201)
        self.assertIn("Question added", str(response.data))

    def test_answer_creation(self):
        """Test API can create a question (POST request)"""
        response = self.app.post('api/v1/questions', content_type='application/json',
                                 data=json.dumps(post_question1))
        response = self.app.post('api/v1/questions/1/answers', content_type='application/json',
                                 data=json.dumps(post_answer1))
        self.assertEqual(response.status_code, 201)
        self.assertIn("Answer added", str(response.data))

    def test_get_all_questions(self):
        """Test StackOver FlowLite API can get all (GET request)."""
        response = self.app.get('/api/v1/questions')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['questions']), 1)
    
    def test_get_question_byId(self):
        """Test API can fetch a question by using it's id."""
        response = self.app.get('/api/v1/questions/1')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)

    def test_api_can_get_error_if_title_is_integer(self):
        """Test API can get error if title is integer (POST request)"""
        response = self.app.post('api/v1/questions', content_type='application/json',
                                 data=json.dumps(post_question3))
        self.assertEqual(response.status_code, 400)

    def test_api_can_get_error_if_title__empty(self):
        """Test API can get error if title is empty (POST request)"""
        response = self.app.post('api/v1/questions', content_type='application/json',
                                 data=json.dumps(post_question4))
        self.assertEqual(response.status_code, 400)

    def test_api_can_get_error_if_body_empty(self):
        """Test API can get error if body is empty (POST request)"""
        response = self.app.post('api/v1/questions', content_type='application/json',
                                 data=json.dumps(post_question5))
        self.assertEqual(response.status_code, 400)

    def test_api_can_get_error_if_body_integer(self):
        """Test API can get error if body is integer (POST request)"""
        response = self.app.post('api/v1/questions',
                                 content_type='application/json',
                                 data=json.dumps(post_question6))
        self.assertEqual(response.status_code, 404)

    
