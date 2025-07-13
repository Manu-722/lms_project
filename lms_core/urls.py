"""
URL configuration for lms_core project.
 
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from lms_core.views import auth_view, dashboard_view, profile_view
from django.contrib.auth.views import LogoutView
from .views import submit_assignment, my_submissions, all_submissions






urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('auth/', auth_view, name='auth'),
    path('profile/', profile_view, name='profile'),


    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('courses/', include('courses.urls')),
    path('communication/', include('communication.urls')),
    path('assignments/', include('assignments.urls')),
    # path('assignments/submit/', submit_assignment, name='submit_assignment'),
    path('api/', include('assignments.urls')),

    
    path('assignments/submit/', submit_assignment, name='submit_assignment'),
    path('assignments/my-submissions/', my_submissions, name='my_submissions'),
    path('assignments/all-submissions/', all_submissions, name='all_submissions'),
    


    

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='auth'), name='logout'),

    


]


from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)