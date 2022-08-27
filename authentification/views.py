from multiprocessing import context
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.models import User
import json
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage

# Create your views here.

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentification/register.html')
    
    def post(self, request):
        #get user data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        #context variable
        context={
            'fieldValues': request.POST
        }
        
        
        #validate informations
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password Too short')
                    return render(request, 'authentification/register.html',context)
                #create the user account
                user = User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.save()
                email_subject = 'Activate your account'
                email_body =''
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'saidbouferriche@gmail.com',
                    [email],
                    )
                email.send(fail_silently=True)
                messages.success(request,'Successfilly registrated')
        return render(request, 'authentification/register.html',context)

    
class UsernameValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        username=data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should contain only alphabetics characters'}, status=400)
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_error': 'username already taken, choose a nother one'}, status=409)

        return JsonResponse({'username_valid': True})
    
    
class EmailValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        email=data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'email is invalid'}, status=400)
        if User.objects.filter(email = email).exists():
            return JsonResponse({'email_error': 'email already taken, choose a nother one'}, status=409)

        return JsonResponse({'email_valid': True})
        