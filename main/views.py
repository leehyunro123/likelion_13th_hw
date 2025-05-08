from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import *
# Create your views here.

def mainpage(request):
    context = {
        'generation': 13,
        'info': {'weather': '좋음', 'feeling': '배고픔(?)', 'note': '아기사자 화이팅!'},
        'shortKeys': [
            '들여쓰기: Tab',
            '내어쓰기: Shift + Tab',
            '주석 처리: 윈도우 - Ctrl + /, 맥 - command + /',
            '자동 정렬: Shift + Alt + F or Ctrl + K + F',
            '한 줄 이동: Alt + 방향키(위/아래)',
            '한 줄 삭제: Ctrl + Shift + k or Ctrl + x',
            '같은 단어 전체 선택: Ctrl + Shift + L'
        ]
    }
    return render(request, 'main/mainpage.html', context)

def secondpage(request):
    blogs = Blog.objects.all()
    posts = Post.objects.all()
    context = {
        'blogs': blogs,
        'posts': posts,
    }
    return render(request, 'main/secondpage.html', context)


def new_blog(request):
    blogs = Blog.objects.all()
    return render(request, 'main/new-blog.html')

def detail(request, id):
    blog = get_object_or_404(Blog, pk=id)
    return render(request, 'main/detail.html', {'blog': blog},)

def create(request):
    new_blog = Blog()

    new_blog.title = request.POST['title']
    new_blog.writer = request.POST['writer']
    new_blog.content = request.POST['content']
    new_blog.pub_date = timezone.now()
    new_blog.image = request.FILES.get('image')

    new_blog.save()

    return redirect('main:detail', new_blog.id)

def edit(request, id):
    edit_blog = Blog.objects.get(pk=id)
    return render(request, 'main/edit.html', {'blog': edit_blog})

def update(request, id):
    update_blog = Blog.objects.get(pk=id)
    update_blog.title = request.POST['title']
    update_blog.writer = request.POST['writer']
    update_blog.content = request.POST['content']
    update_blog.pub_date = timezone.now()


    update_blog.save()
    return redirect('main:detail', update_blog.id)

def create2(request):
    new_post = Post()

    new_post.title = request.POST['title']
    new_post.writer = request.POST['writer']
    new_post.content = request.POST['content']
    new_post.pub_date = timezone.now()
    new_post.image = request.FILES.get('image')

    new_post.save()

    return redirect('main:detail', new_post.id)

def new_post(request):
    return render(request, 'main/post.html')

def detail2(request, id):
    post = get_object_or_404(Post, pk=id)
    post.views += 1
    post.save(update_fields=['views'])
    return render(request, 'main/detail2.html', {'post': post},)

def edit2(request, id):
    edit_post = Post.objects.get(pk=id)
    return render(request, 'main/edit2.html', {'post': edit_post})

def update2(request, id):
    update_post = Post.objects.get(pk=id)
    update_post.title = request.POST['title']
    update_post.writer = request.POST['writer']
    update_post.content = request.POST['content']
    update_post.pub_date = timezone.now()
    update_post.image = request.FILES.get('image')
    update_post.views = request.POST['views']
    update_post.save()

def delete(request, id):
    delete_post= Post.objects.get(pk=id)
    delete_post.delete()
    return redirect('main:secondpage')
