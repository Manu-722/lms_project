from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import EmailUpdateForm, SubmissionForm


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
from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import EmailUpdateForm


@login_required
def profile_view(request):
    user = request.user
    email_form = EmailUpdateForm(instance=user)
    password_form = PasswordChangeForm(user=user)

    if request.method == 'POST':
        if 'update_email' in request.POST:
            email_form = EmailUpdateForm(request.POST, instance=user)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, 'Email updated successfully.')
                return redirect('profile')

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully.')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the errors below.')

    return render(request, 'profile.html', {
        'user': user,
        'email_form': email_form,
        'password_form': password_form
    })
from assignments.models import Submission
from django.contrib.auth.decorators import login_required

@login_required
def my_submissions(request):
    submissions = Submission.objects.filter(student=request.user)
    return render(request, 'my_submissions.html', {'submissions': submissions})
@login_required
def all_submissions(request):
    if request.user.role != 'instructor':
        return redirect('dashboard')
    submissions = Submission.objects.select_related('assignment', 'student')
    return render(request, 'all_submissions.html', {'submissions': submissions})

@login_required
def submit_assignment(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.save()
            return redirect('assignment_dashboard')  
    else:
        form = SubmissionForm()
    return render(request, 'submit.html', {'form': form})
