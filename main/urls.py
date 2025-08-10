from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("homepage/", views.homepage, name="homepage"),
    path("blog_post/<int:pk>/", views.blog_post_details, name="blog_post_details"),
    path("register_user/", views.register_user, name="register_user"),
    path("login_user/", views.login_user, name="login_user"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path("blog_create/", views.blog_create, name="blog_create"),
    path("blog_update/<int:pk>/", views.blog_update, name="blog_update"),
    path("blog_delete/<int:pk>/", views.blog_delete, name="blog_delete"),
    path("add_comment/<int:pk>/", views.add_comment, name="add_comment"),
    path("like_post/<int:post_id>/", views.like_post, name="like_post"),
    path("user/<str:username>/", views.profile_detail, name="profile_detail"),
    path("categories_list/", views.categories_list, name="categories_list"),
    path(
        "category_posts/<int:category_id>/", views.category_posts, name="category_posts"
    ),
]
