from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages

User = get_user_model()

@login_required
def dashboard_view(request):
    role = request.user.role
    return render(request, 'dashboard.html', {'role': role})

def auth_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_exists = User.objects.filter(username=username).exists()

        if user_exists:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Incorrect password. Try again.')
        else:
            user = User.objects.create_user(username=username, password=password, role='student')
            login(request, user)
            messages.success(request, 'Account created. Welcome!')
            return redirect('dashboard')

    return render(request, 'auth.html')