from django.urls import path
from .views import CourseListCreateView, EnrollmentCreateView, MyEnrolledCoursesView, MyTaughtCoursesView, LectureCreateView, AssignmentCreateView, CourseLecturesView, CourseAssignmentsView, SubmissionCreateView, GradeSubmissionView, MySubmissionsView, CourseSubmissionsView, NewGradesView, MarkGradesAsSeenView, my_submissions_view


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
    path('my-submissions/', my_submissions_view, name='my-submissions'),
    # path('my-progress/', progress_view, name='student-progress'),


]
from .views import StudentProgressView

urlpatterns += [
    path('my-progress/', StudentProgressView.as_view(), name='student-progress'),
    path('my-new-grades/', NewGradesView.as_view(), name='new-grades'),
    path('mark-grades-seen/', MarkGradesAsSeenView.as_view(), name='mark-grades-seen'),

]

