import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_core.settings')
django.setup()

from users.models import User
from courses.models import Course, Schedule, Enrollment
from assignments.models import Assignment
from communication.models import Announcement

# Clear existing data
User.objects.all().delete()
Course.objects.all().delete()
Assignment.objects.all().delete()
Announcement.objects.all().delete()

# Create users
admin = User.objects.create_superuser(username='admin', password='admin123', role='admin')
instructor = User.objects.create_user(username='instructor1', password='pass123', role='instructor')
student1 = User.objects.create_user(username='student1', password='pass123', role='student')
student2 = User.objects.create_user(username='student2', password='pass123', role='student')

# Create course
course = Course.objects.create(title='Intro to Python', description='Learn Python basics.', instructor=instructor)
Schedule.objects.create(course=course, day='Monday', time='10:00')

# Enroll students
Enrollment.objects.create(student=student1, course=course)
Enrollment.objects.create(student=student2, course=course)

# Create assignment
Assignment.objects.create(
    title='Python Basics Assignment',
    description='Write a script that prints "Hello, World!"',
    course=course,
    due_date=timezone.now() + timedelta(days=7)
)

# Create announcement
Announcement.objects.create(
    title='Welcome!',
    message='Welcome to the Python course. Let’s get started!',
    author=instructor
)

print("Seed data created successfully.")