from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    role = request.user.role
    context = {'role': role}
    return render(request, 'dashboard.html', context)