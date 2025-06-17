from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from main.models import Post, Blog

# Create your views here.
def mypage(request,id):
    print(f"Received ID: {id}, Type: {type(id)}")
    user = get_object_or_404(User, pk=id)
    posts = Post.objects.filter(writer=user)
    context = {
        'user': user,
        'posts': posts,
    }
    return render(request, 'users/mypage.html', context)

def follow(request, id):
    user = request.user
    follow_user = get_object_or_404(User, pk=id)
    is_follower = user.profile in follow_user.profile.followers.all()
    if is_follower:
        user.profile.followings.remove(follow_user.profile)
    else:
        user.profile.followings.add(follow_user.profile)
    return redirect('users:mypage', follow_user.id)