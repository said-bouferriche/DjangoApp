from cgitb import reset
from lib2to3.pgen2 import token
import logging
from multiprocessing import context
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.models import User
import json
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from .utils import token_generator
from django.contrib import auth


# Create your views here.


    
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
                user.is_active=False
                user.set_password(password)
                user.save()
                
                domain = get_current_site(request).domain
                uidb64=urlsafe_base64_encode(force_bytes(user.pk))
                link=reverse('activate',kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user)})                
                activate_url = 'http://' +domain+ link
                
                
                
                
                
                email_subject = 'Activate your account'
                email_body ='Hi' + user.username + 'Presse the link to register \n' + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'saidbouferriche@gmail.com',
                    [email],
                    )
                email.send(fail_silently=True)
                messages.success(request,'Successfilly registrated')
        return render(request, 'authentification/register.html',context)

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id=force_str(urlsafe_base64_decode(uidb64))
            logging.info('the id of the user id ' + str(id) )
            user = User.objects.get(pk=id)
            if not token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return redirect('login'+'?message'+'user already activated')
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            
        except Exception as e:
            pass
        messages.success(request, 'Account Activated Successfully')
        
        return redirect('login')
    
    
class LoginView(View):
    def get(self, request):
        return render(request, 'authentification/login.html')
    
    def post(self, request):
        username=request.POST['username']
        password=request.POST['password']
        
        if username and password:
            user = auth.authenticate(username=username, password=password)
            
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + user.username)
                    return redirect('expenses')
                
                else:
                    messages.error(request, 'Account is not active, please check your email')
                    return render(request, 'authentification/login.html')

            
            else:
                messages.error(request, 'Invalid Credentials')
                return render(request, 'authentification/login.html')
        
        else:
            messages.error(request, 'Please fill all fields')
            return render(request, 'authentification/login.html')
        
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'Successifilly logout')
        return(redirect('login'))
    
