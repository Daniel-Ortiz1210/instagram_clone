from django.contrib import admin
from .models import User, Follow, Post, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(Comment)