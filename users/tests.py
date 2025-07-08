from django.test import TestCase
from users.models import User


# Create your tests here.
class UserModelTest(TestCase):
    def test_create_student_user(self):
        user = User.objects.create_user(username='student1', password='pass123', role='student')
        self.assertEqual(user.role, 'student')
        self.assertTrue(user.check_password('pass123'))
