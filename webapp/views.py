from django.shortcuts import render
from django.http import HttpResponse

from webapp.models import *
from .forms import *
from datetime import datetime

def base(request):
    #User.objects.all().delete()
    request.session.flush()

    return render(request, "web/base.html")

def signup(request):
    if request.method == 'POST':
        tempusername = request.POST.get('username')
        tempfirstname = request.POST.get('firstname')
        templastname = request.POST.get('lastname')              
        tempemail = request.POST.get('email')
        temppassword = request.POST.get('password') 
        tempblogtitle = request.POST.get('blogtitle') 

        newuser = User(username=tempusername, firstName=tempfirstname, lastName=templastname,
         email=tempemail, password=temppassword)
        newuser.save()

        newblog = Blog(blogTitle=tempblogtitle, user=newuser)
        newblog.save()

        return render(request, 'web/base.html')
        
    else:
        return render(request, 'web/signup.html')

def login(request):
    if request.method == 'POST':
        loginname = request.POST.get('loginname')      
        loginpassword = request.POST.get('loginpassword')
        try:
            tempuser = User.objects.get(username=loginname)        
            if tempuser.password == loginpassword:                                              
                loginblog = Blog.objects.get(user_id=tempuser.id)

                request.session['logged_user_id'] = tempuser.id

                posts = Post.objects.filter(user_id=tempuser.id).order_by('-created_on')
                return render(request, 'web/blog_page.html', 
                {'blogtitle':tempuser.blog.blogTitle,
                 'loginname':tempuser.username, 
                 'posts':posts})
            else:
                return HttpResponse("wrong password!", content_type='text/plain')
        except User.DoesNotExist:
            return HttpResponse("User not exist.", content_type='text/plain')     

    else:
        return render(request, 'web/login.html')

def delete(request):
    if request.method == 'POST':
        name = request.POST.get('loginname')     
        password = request.POST.get('loginpassword')
        try:
            tempname = User.objects.get(username=name)
            print(tempname)
            if tempname.password == password:
                User.objects.get(username=name).delete()
                return render(request, 'web/base.html')
            else:
                return HttpResponse("wrong password!", content_type='text/plain')
        except User.DoesNotExist:
            return HttpResponse("User not exist.", content_type='text/plain')         
    else:
        return render(request, 'web/delete.html')

def blog_page(request):  
    current_user_id = request.session.get('logged_user_id')
    current_user = User.objects.get(id=current_user_id)

    posts = Post.objects.filter(user_id=current_user_id).order_by('-created_on')
    
    return render(request, 'web/blog_page.html', 
    {'blogtitle':current_user.blog.blogTitle,
     'loginname':current_user.username,
     'posts':posts})

def post_page(request):
    if request.method == 'POST':
        current_user_id = request.session.get('logged_user_id')
        current_user = User.objects.get(id=current_user_id)           
        title = request.POST.get('new_title')  
        body = request.POST.get('new_body') 
        tagInput = request.POST.get('tags') 
        print(tagInput)

        new_post = Post(user=current_user, postTitle=title, postBody=body, created_on=datetime.now())
        new_post.save() 

        if tagInput is not None:
            tags = tagInput.split('#')
            for tag in tags:
                newTag = Tag(tags = tag, post = new_post)
                newTag.save() 
        
        posts = Post.objects.filter(user_id=current_user_id).order_by('-created_on')
        return render(request, 'web/blog_page.html', 
        {'blogtitle':current_user.blog.blogTitle,
        'loginname':current_user.username,
        'posts':posts})         
    else:
        return render(request, 'web/post_page.html')

def post_view(request, post_id):
    if request.method == "POST":
        comment_body = request.POST.get('comment')    

        current_user_id = request.session.get('logged_user_id')
        current_user = User.objects.get(id=current_user_id)
        current_post = Post.objects.get(id = post_id)
        request.session['current_post_id'] = post_id

        new_comment = Comment(user = current_user, post = current_post, commentBody = comment_body, created_on=datetime.now())
        new_comment.save()

        comments = Comment.objects.filter(post = current_post)

        context = {
             'post': current_post,
             'comments': comments
        }
        return render(request, 'web/post_view.html', context)
    else:
        post = Post.objects.get(id = post_id)
        request.session['current_post_id'] = post_id
        comments = Comment.objects.filter(post = post).order_by('-created_on')
        
        context = {
            'post': post,
            'comments': comments,
        }
        return render(request, 'web/post_view.html', context)

def user_profile(request, user_id):     
    user = User.objects.get(id=user_id)
    current_post_id = request.session.get('current_post_id')
    context = {
        'user': user,
        'postid': current_post_id
    }
    return render(request, 'web/user_profile.html',  context)

def user_blog(request, user_id):     
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(user_id=user_id).order_by('-created_on')
    context = {
        'user': user,
        'posts': posts
    }
    return render(request, 'web/user_blog.html',  context)
    

def search(request):
    if request.method =="GET":
        form = Search(request.GET)
        if form.is_valid():
            tagInput = form.cleaned_data['search']

            tags = filter(None, tagInput.split('#'))

            tagQ = set()
            for tag in tags:
                q = Tag.objects.filter(tags = tag)
                for post in q:
                    tagQ.add(post)
                
            posts = set()
            for tag in tagQ:
                posts.add(tag.post)
            
            context = {
                'posts': posts
            }
            return render(request, 'web/search.html',  context)
    return render(request, 'web/search.html')


def public_posts(request):
    current_user_id = request.session.get('logged_user_id')
    current_user = User.objects.get(id=current_user_id)

    if request.method =="POST" and 'likebutton' in request.POST:
        current_post_id = request.POST.get('likebutton')
        current_post = Post.objects.get(id=current_post_id)       
        try:
            likeobject = LikePost.objects.get(user_id=current_user_id, post_id=current_post_id)
            if likeobject.is_like == True:
                current_post.likes -= 1
                likeobject.delete()
                current_post.save()
            else:
                likeobject.is_like = True                
                current_post.dislikes -= 1
                current_post.likes += 1
                likeobject.save()
                current_post.save()
        except LikePost.DoesNotExist:
            new_like_post = LikePost(is_like=True, post=current_post, user=current_user, created_on=datetime.now())
            current_post.likes += 1
            current_post.save()
            new_like_post.save()

        all_posts = Post.objects.all()
        posts = all_posts.exclude(user_id=current_user_id)
        context = {
            'posts': posts
        }
        return render(request, 'web/public_posts.html', context)

    elif request.method =="POST" and 'dislikebutton' in request.POST:
        current_post_id = request.POST.get('dislikebutton')
        current_post = Post.objects.get(id=current_post_id) 
        try:
            likeobject = LikePost.objects.get(user_id=current_user_id, post_id=current_post_id)
            if likeobject.is_like == True:
                likeobject.is_like = False
                current_post.likes -= 1
                current_post.dislikes += 1
                current_post.save()
                likeobject.save()
            else:
                current_post.dislikes -= 1
                likeobject.delete()
                current_post.save()
        except LikePost.DoesNotExist:
            new_like_post = LikePost(is_like=False, post=current_post, user=current_user, created_on=datetime.now())
            current_post.dislikes += 1
            current_post.save()
            new_like_post.save()

        all_posts = Post.objects.all()
        posts = all_posts.exclude(user_id=current_user_id)
        context = {
            'posts': posts
        }
        return render(request, 'web/public_posts.html', context)
   
    else:
        all_posts = Post.objects.all()
        posts = all_posts.exclude(user_id=current_user_id)
        context = {
            'posts': posts
        }
        return render(request, 'web/public_posts.html', context)


def profile(request):
    current_user_id = request.session.get('logged_user_id')
    current_user = User.objects.get(id=current_user_id)

    if request.method =="POST":
        new_firstname = request.POST.get('firstname')
        new_lastname = request.POST.get('lastname') 
        new_password = request.POST.get('password')
        new_blogtitle = request.POST.get('blogtitle')

        current_user.firstName = new_firstname
        current_user.lastName = new_lastname
        current_user.password = new_password
        current_user.blog.blogTitle = new_blogtitle
        current_user.save()
        current_user.blog.save()

        posts = Post.objects.filter(user_id=current_user_id).order_by('-created_on')
    
        return render(request, 'web/blog_page.html', 
        {'blogtitle':current_user.blog.blogTitle,
        'loginname':current_user.username,
        'posts':posts})
    else:
        context = {
            'user': current_user
        }
        return render(request, 'web/profile.html',  context)
