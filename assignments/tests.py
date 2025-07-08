from django.test import TestCase
from users.models import User
from courses.models import Course
from assignments.models import Assignment
from django.utils import timezone
from datetime import timedelta



# Create your tests here.
class AssignmentModelTest(TestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(username='instructor1', password='pass123', role='instructor')
        self.course = Course.objects.create(title='Science', description='Basics', instructor=self.instructor)

    def test_assignment_creation(self):
        due = timezone.now() + timedelta(days=7)
        assignment = Assignment.objects.create(title='Lab Report', description='Write a report', course=self.course, due_date=due)
        self.assertTrue(assignment.due_date > timezone.now())
