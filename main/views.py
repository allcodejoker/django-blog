from django.shortcuts import render, redirect
from .models import BlogPost, Category, Comment, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404

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

def blog_create(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            title = request.POST["title"]
            blog_image = request.FILES.get("blog_image")
            description = request.POST["description"]
            category = request.POST["category"]

            category_object = Category.objects.get(name=category)

            new_post = BlogPost.objects.create(user=current_user, title=title, blog_image=blog_image, description=description, category=category_object)
            new_post.save()
            print("Post Created!!!")
            return redirect('homepage')
        
        else:
            categories = Category.objects.all()
            return render(request, 'blog_create.html', {'categories': categories})

    else:
        print("Not logged in")
        return redirect('homepage')

def blog_update(request, pk):
    if request.user.is_authenticated:
        blog_post = BlogPost.objects.get(id=pk)
        categories = Category.objects.all()
        if request.user == blog_post.user:
            if request.method == "POST":
                title = request.POST["title"]
                blog_image = request.FILES.get("blog_image")
                description = request.POST["description"]
                category = request.POST["category"]

                blog_post.title = title
                blog_post.description = description
                blog_post.blog_image = blog_image

                category_object = Category.objects.get(name=category)
                blog_post.category = category_object

                blog_post.save()
                return redirect("blog_post_details", pk=blog_post.pk)
            else:
                return render(request, 'blog_update.html', {'categories': categories, "blog_post": blog_post})
        else:
            return redirect("blog_post_details", pk=blog_post.pk)
    else:
        print("You are not logged in!!!")
        return redirect("homepage")
    
def blog_delete(request, pk):
    if request.user.is_authenticated:
        blog_post = BlogPost.objects.get(id=pk)
        if request.user == blog_post.user:
            if request.method == "POST":
                blog_post.delete()
                print("You deleted a blog post!!!")
                return redirect('homepage')
            else:
                print("You need to use a button!!!")
                return redirect("blog_post_details", pk=blog_post.pk)
        else:
            print("You didn't make this post")
    else:
        return redirect("homepage")

def add_comment(request, pk):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            title = request.POST["title"]
            body = request.POST["body"]

            commented_post = BlogPost.objects.get(id=pk)

            new_comment = Comment.objects.create(user=current_user, title=title, body=body, blog_post=commented_post)
            new_comment.save()
            print("Comment Created!!!")
            return redirect('blog_post_details', pk=commented_post.pk)
        
        else:
            return render(request, 'add_comment.html')

    else:
        print("Not logged in")
        return redirect('homepage')

def like_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    blog_post = BlogPost.objects.get(id=post_id)

    if request.user in blog_post.likes.all():
        blog_post.likes.remove(request.user)
    else:
        blog_post.likes.add(request.user)

    return redirect('blog_post_details', pk=blog_post.pk)

@login_required
def profile_detail(request, username):
    owner = User.objects.filter(username=username).first() # returns None if User not found which you can debug later on with
    if not owner:
        raise Http404("User not found")

    try:
        profile = owner.profile
    except Profile.DoesNotExist:
        raise Http404("Profile not found")

    is_following = profile.followers.filter(id=request.user.id).exists()

    if request.method == "POST" and owner != request.user: # follow button if owner is NOT currently logged in user
        if is_following:
            profile.followers.remove(request.user)
        else:
            profile.followers.add(request.user)
        return redirect(f"/user/{username}/")

    posts = BlogPost.objects.filter(user=owner).order_by("-id")

    return render(request, "user_profile.html", {
        "owner": owner,
        "profile": profile,
        "posts": posts,
        "is_following": is_following,
    })
