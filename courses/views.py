from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Course, Enrollment, Lecture, Assignment, Submission
from .serializers import CourseSerializer, EnrollmentSerializer, LectureSerializer, AssignmentSerializer, SubmissionSerializer
from users.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError



# Create your views here.
class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'instructor'

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsInstructor()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

class EnrollmentCreateView(generics.CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsStudent]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
class MyEnrolledCoursesView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return [enrollment.course for enrollment in Enrollment.objects.filter(student=user)]
        return []
class MyTaughtCoursesView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'instructor':
            return Course.objects.filter(instructor=user)
        return []
    
class LectureCreateView(generics.CreateAPIView):
    serializer_class = LectureSerializer
    permission_classes = [IsInstructor]

    def perform_create(self, serializer):
        course_id = self.request.data.get('course')
        course = Course.objects.get(id=course_id)
        if course.instructor != self.request.user:
            raise PermissionDenied("You are not the instructor for this course.")
        serializer.save(course=course)

class AssignmentCreateView(generics.CreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsInstructor]

    def perform_create(self, serializer):
        course_id = self.request.data.get('course')
        course = Course.objects.get(id=course_id)
        if course.instructor != self.request.user:
            raise PermissionDenied("You are not the instructor for this course.")
        serializer.save(course=course)

class CourseLecturesView(generics.ListAPIView):
    serializer_class = LectureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Lecture.objects.filter(course_id=course_id)

class CourseAssignmentsView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Assignment.objects.filter(course_id=course_id)
    
class SubmissionCreateView(generics.CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsStudent]

    def perform_create(self, serializer):
        assignment_id = self.request.data.get('assignment')
        assignment = Assignment.objects.get(id=assignment_id)

        # Prevent duplicate submissions
        if Submission.objects.filter(assignment=assignment, student=self.request.user).exists():
            raise ValidationError("You have already submitted this assignment.")

        serializer.save(student=self.request.user, assignment=assignment)