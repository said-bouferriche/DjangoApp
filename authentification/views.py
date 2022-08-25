from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.models import User
import json
# Create your views here.

class RegistrationView(View):
    def get(self, request):
        return render(request,'authentification/register.html')

    
class UsernameValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        username=data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should contain only alphabetics characters'}, status=400)
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_error': 'username already taken, choose a nother one'}, status=409)

        return JsonResponse({'username_valid': True})
        