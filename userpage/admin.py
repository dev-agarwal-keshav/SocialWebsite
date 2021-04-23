from django.contrib import admin
from .models import Post, Profile, Like, Following, Comment
# Register your models here.

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Like)
admin.site.register(Following)
admin.site.register(Comment)