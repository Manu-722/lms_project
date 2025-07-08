from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, EnrollmentViewSet, ScheduleViewSet, course_list_view, course_detail_view

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'schedules', ScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('list/', course_list_view, name='course_list'),
    path('detail/<int:pk>/', course_detail_view, name='course_detail'),
]