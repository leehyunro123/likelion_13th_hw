from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User

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
    try:
        blog_writer = User.objects.get(username=blog.writer)
    except User.DoesNotExist:
        blog_writer = None
    return render(request, 'main/detail.html', {'blog': blog, 'blog_writer': blog_writer},)

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
    if request.user.is_authenticated:
        new_post = Post()

        new_post.title = request.POST['title']
        new_post.writer = request.user
        new_post.content = request.POST['content']
        new_post.pub_date = timezone.now()
        new_post.image = request.FILES.get('image')

        new_post.save()

        words = new_post.content.split()
        tag_list = []

        for w in words:
            if len(w) > 0 and w[0] == '#':
                tag_list.append(w[1:])
        for t in tag_list:
            tag, boolean = Tag.objects.get_or_create(name=t)
            new_post.tags.add(tag.id)
        return redirect('main:detail2', new_post.id)
    else:
        return redirect('account:login')

def new_post(request):
    return render(request, 'main/post.html')

def detail2(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'GET':
        comments = Comment.objects.filter(post=post)
        return render(request, 'main/detail2.html', {'post': post, 'comments': comments})
    elif request.method == 'POST':
        new_comment = Comment()
        new_comment.post = post
        new_comment.writer = request.user
        new_comment.content = request.POST['content']
        new_comment.pub_date = timezone.now()
        new_comment.save()
        return redirect('main:detail2', id)
    post.views += 1
    post.save(update_fields=['views'])
    return render(request, 'main/detail2.html', {'post': post})

def edit2(request, id):
    edit_post = Post.objects.get(pk=id)
    return render(request, 'main/edit2.html', {'post': edit_post})

def update2(request, id):
    update_post = Post.objects.get(pk=id)
    if request.user.is_authenticated and request.user == update_post.writer:
        update_post.title = request.POST['title']
        update_post.content = request.POST['content']
        update_post.pub_date = timezone.now()
        update_post.views = request.POST.get('views', update_post.views)
        if request.FILES.get('image'):
            update_post.image = request.FILES.get('image')
        
        update_post.tags.clear() 

        words = update_post.content.split()
        tag_list = []

        for w in words:
            if len(w) > 0 and w[0] == '#':
                tag_list.append(w[1:])

        for t in tag_list:
            tag, _ = Tag.objects.get_or_create(name=t)
            update_post.tags.add(tag.id)

        update_post.save()
        Tag.objects.filter(posts=None).delete()
        return redirect('main:detail2', update_post.id)
    return redirect('accounts:login', update_post.id)

def delete(request, id):
    delete_post= Post.objects.get(pk=id)
    delete_post.delete()
    return redirect('main:secondpage')

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'main/tag-list.html',{'tags': tags})
def tag_posts(request, tag_id):
    tag=get_object_or_404(Tag, id=tag_id)
    posts = tag.posts.all()
    return render(request, 'main/tag-post.html',{'tag': tag,'posts': posts})

def likes(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.like.all():
        post.like.remove(request.user)
        post.like_count -= 1
        post.save()
    else:
        post.like.add(request.user)
        post.like_count += 1
        post.save()
    return redirect('main:detail2', post.id)