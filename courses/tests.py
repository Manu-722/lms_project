from django.test import TestCase
from users.models import User
from courses.models import Course


# Create your tests here.
class CourseModelTest(TestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(username='instructor1', password='pass123', role='instructor')

    def test_create_course(self):
        course = Course.objects.create(title='Math 101', description='Intro to Math', instructor=self.instructor)
        self.assertEqual(course.title, 'Math 101')
