from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, smart_auth_view

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', smart_auth_view, name='smart-auth'),
]

