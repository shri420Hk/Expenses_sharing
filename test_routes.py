import unittest
from app import app, db
from models import User, Expense

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Expense App!', response.data)

    def test_create_user(self):
        response = self.app.post('/users', json={
            'email': 'test@example.com',
            'name': 'Test User',
            'mobile_number': '1234567890'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User created successfully', response.data)

    def test_get_user(self):
        with app.app_context():
            user = User(email='test@example.com', name='Test User', mobile_number='1234567890')
            db.session.add(user)
            db.session.commit()

        response = self.app.get(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test@example.com', response.data)

if __name__ == '__main__':
    unittest.main()