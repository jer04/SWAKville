from django.db import models
from datetime import datetime

class User(models.Model):
    username = models.CharField(max_length = 20, unique=True)
    firstName = models.CharField(max_length = 15)
    lastName = models.CharField(max_length = 15)
    email = models.EmailField(max_length = 50, unique=True)
    password = models.CharField(max_length = 45)
    created_on = models.DateTimeField(auto_now_add=True)
    

class Blog(models.Model):
    blogTitle = models.CharField(max_length = 40)
    user = models.OneToOneField(User, on_delete=models.CASCADE,)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postTitle = models.CharField(max_length = 40)
    postBody = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

class Comment(models.Model):
    user = models.ForeignKey(User, null = True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentBody = models.TextField(null = True, max_length = 200)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0) 


class Tag(models.Model):
    tags = models.CharField(max_length = 15)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class LikePost(models.Model):
    is_like = models.BooleanField(default=None)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null = True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now= True) 




    
    
