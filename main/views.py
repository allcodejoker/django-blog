from django.shortcuts import render
from .models import BlogPost, Category

# Create your views here.

def homepage(request):
    blog_posts = BlogPost.objects.all()
    return render(request, 'homepage.html', {'blog_posts': blog_posts})
