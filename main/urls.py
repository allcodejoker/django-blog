from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('homepage/', views.homepage, name="homepage"),
    path('blog_post/<int:pk>/', views.blog_post_details, name="blog_post_details"),
    path('register_user/', views.register_user, name="register_user"),
    path('login_user/', views.login_user, name="login_user"),
    path('logout_user/', views.logout_user, name="logout_user"),
]
