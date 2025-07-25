from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssignmentViewSet, SubmissionViewSet, submit_assignment_view, submit_assignment

router = DefaultRouter()
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', SubmissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('submit/<int:assignment_id>/', submit_assignment_view, name='submit_assignment'),
     path('submit/', submit_assignment, name='submit_assignment'),
]