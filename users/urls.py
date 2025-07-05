from django.urls import path
from .views import UserRegistrationView, ProtectedUserView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('me/', ProtectedUserView.as_view(), name='user-profile'),
]