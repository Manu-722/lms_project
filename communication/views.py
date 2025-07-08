from rest_framework import viewsets
from .models import Announcement, Message
from .serializers import AnnouncementSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

User = get_user_model()

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all().order_by('-created_at')
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-timestamp')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

# Template views
def announcements_view(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'announcements.html', {'announcements': announcements})

def chat_view(request):
    users = User.objects.exclude(id=request.user.id)
    messages = Message.objects.filter(sender=request.user) | Message.objects.filter(recipient=request.user)
    messages = messages.order_by('timestamp')

    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        content = request.POST.get('content')
        if recipient_id and content:
            recipient = User.objects.get(id=recipient_id)
            Message.objects.create(sender=request.user, recipient=recipient, content=content)
            return redirect('chat')

    return render(request, 'chat.html', {'users': users, 'messages': messages})