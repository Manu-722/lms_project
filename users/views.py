from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

User = get_user_model()

# mission_classes = [IsAdminUser]
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def smart_auth_view(request):
    
    has_logged_in = request.session.get('has_logged_in_before', False)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if has_logged_in:
            
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                request.session['has_logged_in_before'] = True
                return redirect('home')
            messages.error(request, "Invalid credentials")
        else:
            
            email = request.POST.get('email')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                messages.error(request, "Passwords do not match")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
            else:
                User.objects.create_user(username=username, password=password, email=email)
                messages.success(request, "Account created. Please log in.")
                request.session['has_logged_in_before'] = True
                return redirect('smart-auth')

    return render(request, 'smart_auth.html', {'has_logged_in': has_logged_in})
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            request.session['has_logged_in_before'] = True
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html', {'has_logged_in': True})
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created. You can now log in.")
            request.session['has_logged_in_before'] = True
            return redirect('login')

    return render(request, 'register.html', {'has_logged_in': False})
