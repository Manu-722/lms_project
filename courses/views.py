from rest_framework import viewsets
from .models import Course, Enrollment, Schedule
from .serializers import CourseSerializer, EnrollmentSerializer, ScheduleSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, get_object_or_404, redirect
from .forms import EnrollmentForm
from users.permissions import IsStudent

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsStudent]

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

# Template views
def course_list_view(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

def course_detail_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    schedule = Schedule.objects.filter(course=course)

    if request.method == 'POST':
        Enrollment.objects.get_or_create(student=request.user, course=course)
        return redirect('course_list')

    return render(request, 'course_detail.html', {
        'course': course,
        'schedule': schedule
    })