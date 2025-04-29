from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('homepage/', views.homepage, name="homepage"),
    path('blog_post/<int:pk>/', views.blog_post_details, name="blog_post_details"),
]
