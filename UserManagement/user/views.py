from django.shortcuts import render
from django.views.generic import View
from user.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
import random
from django.core.mail import send_mail
# Create your views here.


class user_home(View):
    def get(self,request):
        all_user=User.objects.all()
        all_user_info=UserInfo.objects.all()
        d={'all_user':all_user,'all_user_info':all_user_info}
        return render(request,'user/home.html',d)
class  user_register(View):
    def get(self,request):
        EUFO=UserForm()
        EUIFO=UserInfoForm()
        d={'EUFO':EUFO,'EUIFO':EUIFO}
        return render(request,'user/register.html',d)
    def post(self,request):
        UFDO=UserForm(request.POST)
        UIFDO=UserInfoForm(request.POST)
        if UFDO.is_valid() and UIFDO.is_valid():
            pw=request.POST.get('password')
            MUFDO=UFDO.save(commit=False)
            MUFDO.username = UFDO.cleaned_data.get('email')
            MUFDO.set_password(pw)
            MUIFDO=UIFDO.save(commit=False)
            MUIFDO.username=MUFDO
            role = UIFDO.cleaned_data.get('role')
            if role in ('Owner', 'Director'):
                MUFDO.is_staff=True
                MUFDO.is_superuser=True
            MUFDO.save()
            MUIFDO.save()
            email=UFDO.cleaned_data.get('email')
            message=f'{MUFDO.first_name} {MUFDO.last_name}\n \t your registration sucessfully done\n \t welcome to our application'
            send_mail(
                'your registrastion',
                message,
                'kumarmanoj8260910@gmail.com',
                [email],
                fail_silently=False


            )
            return  HttpResponseRedirect(reverse('user_login'))
        return HttpResponse('invalid data')
            
class user_login(View):
    def get(self,request):
        return render(request,'user/login.html')
    def post(self,request):
        un=request.POST.get('mobile')
        pw=request.POST.get('pw')
        AUO=authenticate(username=un,password=pw)
        if AUO:
            login(request,AUO)
            request.session['username']=un
            return HttpResponseRedirect(reverse('user_home'))
        return HttpResponse('not found')
class user_logout(View):
    def get(self,request):
          logout(request)
          return render(request,'user/home.html')  
        
  
        

    
class forget_password(View): 
    def get(self,request):
        return render(request,'user/forget_password.html')
    def post(self,request):
        un=request.POST.get('mobile')
        if un:
             UO=User.objects.get(username=un)
             otp=random.randint(1000,9999)
             request.session['username']=un
             request.session['otp']=otp
             email=UO.email
             mesaage=f'your otp  is : {otp}'
             send_mail( 
                'your otp',
                mesaage,
                'kumarmanoj8260910@gmail.com',
                [email],
                fail_silently=False
             )
             return HttpResponseRedirect(reverse('otp'))
        return    HttpResponse('username not found') 
        
    
class otp(View):
    def get(self,request):
        return render(request,'user/otp.html')
    def post(self,request):
        uotp=request.POST.get('uotp')
        sotp=request.session.get('otp')
        print(uotp)
        print(type(uotp))
        if uotp == str(sotp) :
            return HttpResponseRedirect(reverse('new_password'))
        return HttpResponse('invalid otp')
    
class new_password(View):
    def get(self,request):
         
         return render(request,'user/new_password.html') 
    def post(self,request):
        npw=request.POST.get('npw')   
        cpw=request.POST.get('cpw')   
        if npw == cpw :
            un=request.session.get('username')
            
            if un:
              UO=User.objects.get(username=un)
              UO.set_password(cpw)
              UO.save()
              return HttpResponseRedirect(reverse('customer_login'))
            return HttpResponse('session expired')            
        return HttpResponse('password doesnot match')
      
