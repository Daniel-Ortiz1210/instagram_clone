from django.db import models
from user.models import User


class Post(models.Model):
    desc = models.CharField(max_length=250, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='static/', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post')
    likes = models.ManyToManyField(User, related_name='like')
    comments = models.ManyToManyField('Comment', related_name='comment')
    
    class Meta:
        ordering = ['posted_at']

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    content = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)