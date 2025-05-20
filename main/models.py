from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name=models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=50)
    writer = models.CharField(max_length=30)
    content = models.TextField()
    pub_date = models.DateTimeField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)

    def __str__(self):
        return self.title
    
    def summary(self):
        return self.content[:20]

class Post(models.Model):
    title = models.CharField(max_length=50)
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    content = models.TextField()
    pub_date = models.DateTimeField()
    image = models.ImageField(upload_to='post/', blank=True, null=True)
    views = models.PositiveIntegerField(default=0, help_text="조회수")
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    def __str__(self):
        return self.title
    
    def summary(self):
        return self.content[:20]
class Comment(models.Model):
    content = models.TextField()
    pub_date = models.DateTimeField()
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=False, blank=False, on_delete=models.CASCADE)
    
    def str (self):
        return self.post.title + " : " + self.content[:20] + "by" + self.writer.profile.nickname
