from django.urls import path
from .views import CourseListCreateView, EnrollmentCreateView, MyEnrolledCoursesView, MyTaughtCoursesView, LectureCreateView, AssignmentCreateView, CourseLecturesView, CourseAssignmentsView, SubmissionCreateView, GradeSubmissionView, MySubmissionsView, CourseSubmissionsView


urlpatterns = [
    path('', CourseListCreateView.as_view(), name='course-list-create'),
    path('enroll/', EnrollmentCreateView.as_view(), name='enroll'),
    path('my-courses/', MyEnrolledCoursesView.as_view(), name='my-courses'),
    path('my-teaching/', MyTaughtCoursesView.as_view(), name='my-teaching'),
    path('lectures/create/', LectureCreateView.as_view(), name='create-lecture'),
    path('assignments/create/', AssignmentCreateView.as_view(), name='create-assignment'),
    path('<int:course_id>/lectures/', CourseLecturesView.as_view(), name='course-lectures'),
    path('<int:course_id>/assignments/', CourseAssignmentsView.as_view(), name='course-assignments'),
    path('submit/', SubmissionCreateView.as_view(), name='submit-assignment'),
    path('submissions/<int:pk>/grade/', GradeSubmissionView.as_view(), name='grade-submission'),
    path('my-submissions/', MySubmissionsView.as_view(), name='my-submissions'),
    path('<int:course_id>/submissions/', CourseSubmissionsView.as_view(), name='course-submissions'),






]