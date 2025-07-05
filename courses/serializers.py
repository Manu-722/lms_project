from rest_framework import serializers
from .models import Course, Enrollment
from users.models import CustomUser

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'prerequisites', 'instructor']
        read_only_fields = ['instructor']

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_at']
        read_only_fields = ['student', 'enrolled_at']