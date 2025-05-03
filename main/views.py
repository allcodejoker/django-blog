from django.shortcuts import render, redirect
from .models import BlogPost, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.

def homepage(request):
    blog_posts = BlogPost.objects.all()
    return render(request, 'homepage.html', {'blog_posts': blog_posts})

def blog_post_details(request, pk):
    blog_post = BlogPost.objects.get(id=pk)

    return render(request, 'blog_post_details.html', {'blog_post': blog_post})

def register_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password != password2:
            print("Passwords didn't match!")
            return redirect('register_user')

        if User.objects.filter(username=username).exists():
            print("Username already taken!")
            return redirect('register_user')

        try:
            user = User.objects.create(username=username, password=password)
            user.save()
            login(request, user)
            print("Successfully registered!!!")
            return redirect('homepage')
        except Exception as e:
            print(f"Error: {e}")
            return redirect('register_user')

    return render(request, 'register_user.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("Successfully logged in!!!")
            return redirect('homepage')
        else:
            print("Wrong credentions")
            return redirect('login_user')

    return render(request, 'login_user.html')

def logout_user(request):
    logout(request)
    print("Successfully logged out!!!")
    return redirect('login_user')
