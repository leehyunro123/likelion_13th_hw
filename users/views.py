from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from main.models import Blog

# Create your views here.
def mypage(request,id):
    user = get_object_or_404(User, pk=id)
    blogs = Blog.objects.filter(writer=user.username)
    context = {
        'user': user,
        'blogs': blogs,
    }
    return render(request, 'users/mypage.html', context)
        