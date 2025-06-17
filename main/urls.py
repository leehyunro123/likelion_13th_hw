from django.urls import path
from .views import *

app_name = "main"
urlpatterns = [
    path('', mainpage, name="mainpage"),
    path('second', secondpage, name="secondpage"),
    path('new-blog', new_blog, name="new-blog"),
    path('create', create, name="create"),
    path('<int:id>', detail, name="detail"),
    path('edit/<int:id>', edit, name="edit"),
    path('update/<int:id>', update, name="update"),
    path('post', new_post, name="post"),
    path('create2', create2, name="create2"),
    path('post/<int:id>', detail2, name="detail2"),
    path('edit2/<int:id>', edit2, name="edit2"),
    path('update2/<int:id>', update2, name="update2"),
    path('delete/<int:id>', delete, name="delete"),
    path('tag-list', tag_list, name="tag-list"),
    path('tag-posts/<int:tag_id>', tag_posts, name="tag-posts"),
    path('likes/<int:post_id>', likes, name="likes"),
]