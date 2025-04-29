from django.shortcuts import render
from .models import BlogPost, Category

# Create your views here.

def homepage(request):
    blog_posts = BlogPost.objects.all()
    return render(request, 'homepage.html', {'blog_posts': blog_posts})

def blog_post_details(request, pk):
    blog_post = BlogPost.objects.get(id=pk)

    return render(request, 'blog_post_details.html', {'blog_post': blog_post})
