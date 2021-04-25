from django.shortcuts import redirect, render
from .models import *
from django.views import View
from django.contrib import auth

import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core .mail import EmailMessage




from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import account_token_generator
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading
# Create your views here
# username validation 
class UsernameValidationView(View):
    def post(self,request):
        #getting data over a network and turning it to json
        data = json.loads(request.body)
        username = data['username']
        # checking if username is alphannum

        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should contain only alphanumeric characters'},status =403)
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_error':'username already taken,Choose another one'})   
        else:
            return JsonResponse({"username_success":True})    
        
class EmailValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({"email_error": 'email is invalid'}, status = 403)
        if User.objects.filter(email = email).exists():
            return JsonResponse({"email_error":'email already taken,Choose another!'},status = 403)
        return JsonResponse({'email_valid':True})        


class EmailThreading(threading.Thread):
    def __init__(self,email):
        self.email = email
        threading.Thread.__init__(self)
    def run(self):
        self.email.send(fail_silently = False)
class RegisterView(View):
    def get(self,request):
        return render(request,'authentication/register.html')
    def post(self,request):

        # getting the data
        username = request.POST['username']
        email =request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues':request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email):
                if len(password) <6:
                    messages.error(request,"Password too short")
                    return render(request,'authentication/register.html',context)
                else:
                    user = User.objects.create_user(username=username,email=email)
                    user.set_password(password)
                    user.is_active = False
                    user.save()
                    uidb64 =urlsafe_base64_encode(force_bytes(user.pk))
                    domain =get_current_site(request).domain
                    link =reverse('activate', kwargs={'uidb64':uidb64,'token':account_token_generator.make_token(user)})
                    activate_url ='http://'+domain+link
                    email_subject='Activate your account'
                    email_body ='Hi '+ user.username+ ' Please use this link to verify your account\n'+activate_url
                    email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@posts.com',
                    [email],

                    )
                    EmailThreading(email).start()
                    messages.success(request,'Account succesfully created')   
 
        return render(request,'authentication/register.html')

class VerificationView(View):
    def get(self,request,uidb64,token):
        try:
            id =force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            if not account_token_generator.check_token(user,token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            else:
                user.is_active =True 
                user.save()   
                messages.success(request,"Account activated successfully")
                return redirect('login')

        except Exception as e:
            pass    
        return redirect('login')

class LoginView(View):
    def get(self,request):
        return render(request, 'authentication/login.html') 
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request,'Welcome '+user.username+' you can now comment')
                    return redirect('home')

                messages.error(request,'account is not active please check your email to activate')
                return render(request, 'authentication/login.html')

            messages.error(request,'Invalid credentials,Please try again')
            return render(request, 'authentication/login.html') 

        messages.error(request,'Please fill all fields')
        return render(request, 'authentication/login.html')   

class LogoutView(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request,'You have been logged out')
        return redirect('login')

                
class ResetPasswordView(View):
    def get(self,request):
        return render(request, 'authentication/reset_password.html') 

    def post(self,request):
        email = request.POST['email']

        context ={
            'value':request.POST
        }

        if not validate_email(email):
            messages.error(request,'Please supply a valid email')
            return render(request,"authentication/reset_password.html",context)
        
        current_site =get_current_site(request)
        user =User.objects.filter(email=email)
        if  user.exists():
            email_contents ={
                'user':user[0],
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0]),
            }
            # domain = get_current_site(request).domain
            # link = reverse('activate',kwargs ={'uidb64':uidb64,'token':account_token_generator.make_token(user)})
            # activate_link ='http://'+domain + link
            link = reverse('reset_user_password',kwargs={'uidb64':email_contents['uid'],'token':email_contents['token']})

            email_subject = 'Password reset instructions'
            reset_link = 'http://'+ current_site.domain + link
            email_body = 'Hi' + ' Please click the link below to reset your password\n'+ reset_link

            email = EmailMessage(
            email_subject,
            email_body,
            'noreply@activate.com',
            [email],
            )
            EmailThreading(email).start()

        messages.success(request,"We've sent you an email to reset your password")
        return redirect('login')




class CompletePasswordReset(View):
    def get(self,request,uidb64,token):

        context = {
            'uidb64': uidb64,
            'token':token

        }
        try:
            user_id =force_text(urlsafe_base64_decode(uidb64))  
            user = User.objects.get(pk=user_id)    
            
            #prevent using a link multiple times
            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.info(request,'Reset link invalid,Please request a new one') 
                return render(request,'authentication/reset_password.html',context)  
               
        except Exception as error:

            pass
        
        return render(request, 'authentication/set_new_password.html',context) 

    def post(self,request,uidb64,token):
        context = {
            'uidb64': uidb64,
            'token':token

        }

        password = request.POST['password1']
        password2 = request.POST['password2']

        if password !=password2:
            messages.error(request, 'Passwords does not match')
            return render(request, 'authentication/set_new_password.html',context) 
        
        if len(password)<6:
            messages.error(request, 'Passwords too short')
            return render(request, 'authentication/set_new_password.html',context) 
        try:
            user_id =force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Password reset successfull,You can login with the new password")
            return redirect('login')
        except Exception as error:
            messages.info(request,"Oops! something went wrong")
            return render(request, 'authentication/set_new_password.html',context) 

     