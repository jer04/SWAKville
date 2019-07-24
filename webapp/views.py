from django.shortcuts import render
from django.http import HttpResponse

from webapp.models import *
from .forms import NewPost
from datetime import datetime

def base(request):
    #User.objects.all().delete()
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

        #newUserBlog = UserBlog(author=newuser, blog=newblog)
        #newUserBlog.save()
        return render(request, 'web/base.html')
        
    else:
        return render(request, 'web/signup.html')

def login(request):
    if request.method == 'POST':
        loginname = request.POST.get('loginname')      
        loginpassword = request.POST.get('loginpassword')
        try:
            #loginuser = User.objects.filter(username=loginname)
            tempuser = User.objects.get(username=loginname)
            #print(tempname)           
            if tempuser.password == loginpassword:                                              
                loginblog = Blog.objects.get(user_id=tempuser.id)
                #print(tempname.id)
                #print(loginblogID)
                #tempuser = loginblog.user
                #print(tempuser.username)
                #print(tempuser.firstName)
                #logintitile = loginblog.blogTitle
                request.session['logged_user_id'] = tempuser.id
                request.session['logged_blog_title'] = loginblog.blogTitle
                posts = Post.objects.filter(user_id=tempuser.id).order_by('created_on')
                return render(request, 'web/blog_page.html', 
                {'blogtitle':loginblog.blogTitle,
                 'loginname':tempuser.firstName, 
                 'posts':posts})
            else:
                return HttpResponse("wrong password!", content_type='text/plain')
        except User.DoesNotExist:
            return HttpResponse("User not exist.", content_type='text/plain')     

    else:
        return render(request, 'web/login.html')

def home(request):
    return render(request, "web/home.html")

def delete(request):
    if request.method == 'POST':
        name = request.POST.get('loginname')
        #print(loginname)       
        password = request.POST.get('loginpassword')
        #print(loginpassword)
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
    current_blog_title = request.session.get('logged_blog_title')
    #print(current_user_id)
    posts = Post.objects.filter(user_id=current_user_id).order_by('created_on')
    
    #posts = Post.objects.all().order_by('created_on') # grabs all records from the posts database table.
    return render(request, 'web/blog_page.html', 
    {'blogtitle':current_blog_title,
     'loginname':current_user.firstName,
     'posts':posts})

# This posts all the posts in order by date created on the blog page.

def post_page(request):
    if request.method == 'POST':
        form = NewPost(request.POST)
        if form.is_valid():
            current_user_id = request.session.get('logged_user_id')
            current_user = User.objects.get(id=current_user_id)           
            current_blog_title = request.session.get('logged_blog_title')
            
            title = form.cleaned_data['new_title']
            body = form.cleaned_data['new_body']
            new_post = Post(user=current_user, postTitle=title, postBody=body, created_on=datetime.now())
            new_post.save()

            posts = Post.objects.filter(user_id=current_user_id).order_by('created_on')

            return render(request, 'web/blog_page.html', 
            {'blogtitle':current_blog_title,
            'loginname':current_user.firstName,
            'posts':posts})
    else:
        #form = NewPost()
        #return render(request, 'blog/post_page.html', {'form': form})
        return render(request, 'web/post_page.html')
    # return render(request, 'posts/post_page.html')

    
def post_view(request, post_id):
    post = Post.objects.get(postID = post_id)
    context = {
        'post' : post
    }
    return render(request, 'blog/post_view.html', context)

