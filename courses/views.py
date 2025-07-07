from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Course, Enrollment, Lecture, Assignment, Submission
from .serializers import CourseSerializer, EnrollmentSerializer, LectureSerializer, AssignmentSerializer, SubmissionSerializer
from users.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
# from users.permissions import IsInstructor 
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Avg
# from users.permissions import IsStudent
from rest_framework.views import APIView







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

        #  Check if the deadline has passed
        if assignment.due_date < timezone.now():
            raise ValidationError("The deadline for this assignment has passed.")

        #  Prevent duplicate submissions
        if Submission.objects.filter(assignment=assignment, student=self.request.user).exists():
            raise ValidationError("You have already submitted this assignment.")

        serializer.save(student=self.request.user, assignment=assignment)


class GradeSubmissionView(generics.UpdateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsInstructor]

    def perform_update(self, serializer):
        submission = self.get_object()
        if submission.assignment.course.instructor != self.request.user:
            raise PermissionDenied("You are not allowed to grade this submission.")
        serializer.save(graded=True)
    
class MySubmissionsView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Submission.objects.filter(student=self.request.user)
    
class CourseSubmissionsView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsInstructor]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = Course.objects.get(id=course_id)

        if course.instructor != self.request.user:
            raise PermissionDenied("You are not the instructor for this course.")

        return Submission.objects.filter(assignment__course=course)
    
class StudentProgressView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        student = request.user
        submissions = Submission.objects.filter(student=student, grade__isnull=False)

        progress = {}
        for submission in submissions:
            course = submission.assignment.course
            course_id = course.id
            if course_id not in progress:
                progress[course_id] = {
                    "course_title": course.title,
                    "grades": [],
                    "average": 0.0
                }
            progress[course_id]["grades"].append(float(submission.grade))

        # Calculate averages
        for course_id in progress:
            grades = progress[course_id]["grades"]
            progress[course_id]["average"] = round(sum(grades) / len(grades), 2)

        return Response(progress)
class NewGradesView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Submission.objects.filter(student=self.request.user, graded=True)
    
class MarkGradesAsSeenView(APIView):
    permission_classes = [IsStudent]

    def post(self, request):
        submissions = Submission.objects.filter(student=request.user, graded=True)
        submissions.update(graded=False)
        return Response({"detail": "All graded submissions marked as seen."})


from django.shortcuts import render
from .models import Enrollment

def my_courses_view(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(request, 'my_courses.html', {'enrollments': enrollments})
from .models import Assignment, Submission
from django.shortcuts import redirect

def submit_assignment_view(request, assignment_id):
    if request.method == 'POST':
        assignment = Assignment.objects.get(id=assignment_id)
        Submission.objects.create(
            assignment=assignment,
            student=request.user,
            file=request.FILES.get('file')
        )
        return redirect('my-submissions')
from .models import Submission

def my_submissions_view(request):
    submissions = Submission.objects.filter(student=request.user)
    return render(request, 'submissions.html', {'submissions': submissions})