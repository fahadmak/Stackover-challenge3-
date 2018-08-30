import jwt
import json
import unittest
from api.app import create_app
from api.database_handler import DatabaseConnection


class QuestionsTestCase(unittest.TestCase):

    token = 'jghjdfhjgjjkhgjkhdfhjkjgtrygyuhhgdthgjghhfgh'

    def setUp(self):
        self.app = create_app('TESTING')
        self.app.app_context().push()
        self.client = self.app.test_client()
        db = DatabaseConnection()
        db.create_tables()

    # def test_invalid_user_registration_no_name(self):
    #     response = self.client.post('/api/v1/auth/signup', content_type='application/json',
    #                                 data=json.dumps(dict(name="", username="faraqsddss", password="crimnalman22")))
    #     self.assertEqual(response.status_code, 401)
    #     self.assertIn("name is missing", str(response.data))
    def create_token(self):
        response = self.client.post('/api/v1/auth/signup', content_type='application/json',
                                    data=json.dumps(dict(name="pikdddde", username="dffssssdedefffs",
                                                         password="sjshfsdghsgs")))
        payload = {
            'user': dict('username'),
            'exp': dict('password')
        }
        token = jwt.encode(payload, 'secret')
        return token
    
    def test_invalid_user_registration_no_username(self):
        response = self.client.post('/api/v1/auth/signup', content_type='application/json',
                                    data=json.dumps(dict(name="pike hsgssssf", username="", password="crimnalman22" )))
        self.assertEqual(response.status_code, 401)
        self.assertIn("username is missing", str(response.data))
    
    def test_invalid_user_registration_no_password(self):
        response = self.client.post('/api/v1/auth/signup', content_type='application/json',
                                    data=json.dumps(dict(name="pikehfghfgfggdj", username="dffsfghghffgss",
                                                         password="")))
        self.assertEqual(response.status_code, 401)
        self.assertIn("missing password", str(response.data))

    def test_sign_up(self):
        response = self.client.post('/api/v1/auth/signup', content_type='application/json',
                                    data=json.dumps(dict(name="pikdddde", username="dffssssdedefffs",
                                    password="sjshfsdghsgs")))
        self.assertEqual(response.status_code, 201)
        self.assertIn("You have registered successfully", str(response.data))

    def test_log_in(self):
        response = self.client.post('/api/v1/auth/login',
                                    data=json.dumps(dict(username="faraqsddss", password="crimnalman22")))
        self.assertEqual(response.status_code, 201)
        self.assertIn("You have registered successfully", str(response.data))

    def test_post_question(self):
        response = self.client.post('/api/v1/questions', content_type='application/json',
                                    data=json.dumps(dict(title="the outliers", body="what is 10000")))
        self.assertEqual(response.status_code, 201)
        self.assertIn("You have successfully created a question", str(response.data))

    def test_get_question_byid(self):
        resp = self.client.post('/api/v1/questions/1', content_type='application/json',
                                    data=json.dumps(dict(title="the outliers", body="what is 10000", user_id=21 )))
        response = self.client.get('/api/v1/questions/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Question of 1 has been retrieved", str(response.data))

    def test_get_questions(self):
        resp = self.client.post('/api/v1/questions', content_type='application/json',
                                    data=json.dumps(dict(title="the outliers", body="what is 10000", user_id=1)))
        resp2 = self.client.post('/api/v1/questions', content_type='application/json',
                                data=json.dumps(dict(title="the outliers", body="what is 10000", user_id=1)))
        response = self.client.get('/api/v1/questions')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Question of 1 has been retrieved", str(response.data))

    def test_get_questions(self):
        resp = self.client.post('/api/v1/questions', content_type='application/json',
                                    data=json.dumps(dict(title="the outliers", body="what is 10000", user_id=1)))
        resp2 = self.client.post('/api/v1/questions', content_type='application/json',
                                data=json.dumps(dict(title="the outliers", body="what is 10000", user_id=1)))
        response = self.client.get('/api/v1/questions')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Question of 1 has been retrieved", str(response.data))



    def tearDown(self):
        """teardown all initialized variables."""
        self.db = DatabaseConnection()
        self.db.drop_all()
        













# from app import views, app


# class QuestionsTestCase(unittest.TestCase):

#     def setUp(self):
#         self.app = app.test_client()
#         self.app.testing = True
#         self.db = DatabaseConnection()

#     def test_login(self):
#         response = self.app.post('api/v1/questions', content_type='application/json',
#                                 data=json.dumps(post_question1))
# 		self.assertFalse(login('my name'), msg='add user id')
# 		self.assertFalse(login(12), msg='add ')
    
#     def test_question_creation(self):
#         """Test API can create a question (POST request)"""
#         response = self.app.post('api/v1/questions', content_type='application/json',
#                                  data=json.dumps(post_question1))
#         self.assertEqual(response.status_code, 201)
#         self.assertIn("Question added", str(response.data))

#     def test_answer_creation(self):
#         """Test API can create a question (POST request)"""
#         response = self.app.post('api/v1/questions', content_type='application/json',
#                                  data=json.dumps(post_question1))
#         response = self.app.post('api/v1/questions/1/answers', content_type='application/json',
#                                  data=json.dumps(post_answer1))
#         self.assertEqual(response.status_code, 201)
#         self.assertIn("Answer added", str(response.data))

#     def test_get_all_questions(self):
#         """Test StackOver FlowLite API can get all (GET request)."""
#         response = self.app.get('/api/v1/questions')
#         data = json.loads(response.get_data())
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(data['questions']), 1)
    
#     def test_get_question_byId(self):
#         """Test API can fetch a question by using it's id."""
#         response = self.app.get('/api/v1/questions/1')
#         data = json.loads(response.get_data())
#         self.assertEqual(response.status_code, 200)

#     def test_api_can_get_error_if_title_is_integer(self):
#         """Test API can get error if title is integer (POST request)"""
#         response = self.app.post('api/v1/questions', content_type='application/json',
#                                  data=json.dumps(post_question3))
#         self.assertEqual(response.status_code, 400)

#     def test_api_can_get_error_if_title__empty(self):
#         """Test API can get error if title is empty (POST request)"""
#         response = self.app.post('api/v1/questions', content_type='application/json',
#                                  data=json.dumps(post_question4))
#         self.assertEqual(response.status_code, 400)

#     def test_api_can_get_error_if_body_empty(self):
#         """Test API can get error if body is empty (POST request)"""
#         response = self.app.post('api/v1/questions', content_type='application/json',
#                                  data=json.dumps(post_question5))
#         self.assertEqual(response.status_code, 400)

#     def test_api_can_get_error_if_body_integer(self):
#         """Test API can get error if body is integer (POST request)"""
#         response = self.app.post('api/v1/questions',
#                                  content_type='application/json',
#                                  data=json.dumps(post_question6))
#         self.assertEqual(response.status_code, 404)

    
