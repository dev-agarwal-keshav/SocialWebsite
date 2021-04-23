from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.userHome, name="userHome"),
    path('addpost', views.addPost, name="addPost"),
    path('like_dislike', views.likePost, name="like_dislike_post"),
    path('delete/<int:postId>', views.delPost, name="delPost"),
    path('profile/<str:username>', views.userProfile, name="userProfile"),
    path('comment', views.comment, name="comment"),
    path('user/follow/<str:username>', views.follow, name="follow"),
    path('search', views.search, name="search"),
    ]