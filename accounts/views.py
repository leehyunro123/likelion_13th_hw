from django.shortcuts import render, redirect
from django.contrib import auth 
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('main:mainpage')
        
        else:
            return render(request, 'accounts/login.html')
        
    elif request.method == 'GET':
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)  # 로그아웃 처리
    return redirect('main:mainpage')  # 메인 페이지로 리다이렉트
def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm']:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password']
            )
            #age = request.POST['age']
            #mbti = request.POST['mbti']

            #profile = Profile(user=user, age=age, mbti=mbti)
            #profile.save()
            
            auth.login(request, user)
            return redirect('/')
    return render(request, 'accounts/signup.html')