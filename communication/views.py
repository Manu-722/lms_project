from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Message
from courses.models import Submission 
from .serializers import MessageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib import messages as django_messages


# Create your views here.
class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class InboxView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user).order_by('-timestamp')

class MarkMessageAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        message = Message.objects.get(pk=pk)
        if message.recipient != request.user:
            raise PermissionDenied("You can only mark your own messages as read.")
        message.is_read = True
        message.save()
        return Response({"detail": "Message marked as read."})
class SentMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user).order_by('-timestamp')
    

from django.shortcuts import render

def inbox_view(request):
    messages = Message.objects.filter(recipient=request.user)
    return render(request, 'inbox.html', {'messages': messages})

def sent_view(request):
    messages = Message.objects.filter(sender=request.user)
    return render(request, 'sent.html', {'messages': messages})

def progress_view(request):
    submissions = Submission.objects.filter(student=request.user, grade__isnull=False)
    progress = {}
    for s in submissions:
        c = s.assignment.course
        if c.id not in progress:
            progress[c.id] = {"course_title": c.title, "grades": []}
        progress[c.id]["grades"].append(float(s.grade))
    for p in progress.values():
        p["average"] = round(sum(p["grades"]) / len(p["grades"]), 2)
    return render(request, 'progress.html', {'progress': progress})

def submissions_view(request):
    submissions = Submission.objects.filter(student=request.user)
    return render(request, 'submissions.html', {'submissions': submissions})

def compose_message_view(request):
    users = User.objects.all()

    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')
        content = request.POST.get('content')

        try:
            recipient = User.objects.get(id=recipient_id)
            Message.objects.create(sender=request.user, recipient=recipient, content=content)
            django_messages.success(request, "Message sent successfully.")
            return redirect('sent-messages')
        except User.DoesNotExist:
            django_messages.error(request, "Recipient not found.")

    return render(request, 'compose_message.html', {'users': users})
