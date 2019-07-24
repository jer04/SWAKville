from django.db import models
from datetime import datetime

class User(models.Model):
    username = models.CharField(max_length = 20, unique=True)
    firstName = models.CharField(max_length = 15)
    lastName = models.CharField(max_length = 15)
    email = models.EmailField(max_length = 50, unique=True)
    password = models.CharField(max_length = 30)
    #profilePic = models.IntegerField(default = 0)  
    #aboutMe = models.TextField(max_length = 200) 

    #When email is verified, if not then the account will be deleted in 7 days
    #isActive = models.BooleanField()
    #When user wants a private account with no commenting by others ect.  
    #isPrivate = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)
    '''
    def __str__(self):
        return self.username
    '''

class Blog(models.Model):
    blogTitle = models.CharField(max_length = 40)
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    '''
    def __str__(self):
       return self.user.username
    '''
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postTitle = models.CharField(max_length = 40)
    postBody = models.TextField(null=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    '''
    def __str__(self):
        return (self.postTitle, self.blog)
        '''

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentBody = models.CharField(max_length = 200)
    isReply = models.BooleanField()
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0) 
    created_on = models.DateTimeField(auto_now_add=True)
    '''
    def __str__(self):
        return (self.commentBody, self.post)
        '''

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    replyBody = models.CharField(max_length = 200)
    isReply = models.BooleanField()
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0) 
    created_on = models.DateTimeField(auto_now_add=True)
    '''
    def __str__(self):
        return (self.replyBody, self.comment)     
        '''

class Tag(models.Model):
    tags = models.CharField(max_length = 15)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    '''
    def __str__(self):
        return (self.tags, self.post)
        '''

class LikePost(models.Model):
    is_like = models.BooleanField(default=None)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    '''
    def __str__(self):
        return (self.is_like, self.post)
        '''
'''
class LikePost(models.Model):
    is_like = models.BooleanField(default=none)
    user = models.ForeignKey(User, on_delete.models.CASCADE)
    post = models.ForeignKey(Post, on_delete.models.CASCADE)

class LikeComment(models.Model):
    is_like = models.BooleanField(default=none)
    user = models.ForeignKey(User, on_delete.models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete.models.CASCADE)
'''
    
