from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnnouncementViewSet, MessageViewSet, announcements_view, chat_view

router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('announcements/', announcements_view, name='announcements'),
    path('chat/', chat_view, name='chat'),
]