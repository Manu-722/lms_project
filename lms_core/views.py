from django.http import JsonResponse
from django.shortcuts import render

def home(request):
     return render(request, 'home.html') 
    # return JsonResponse({"message": "Welcome to the LMS"})