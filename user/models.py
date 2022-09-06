from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

'''
Prevent self-follow
https://adamj.eu/tech/2021/02/26/django-check-constraints-prevent-self-following/

'''

class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    followers = models.ManyToManyField(
        to='self',
        through='Follow',
        related_name='following_list',
        symmetrical=False
        )
    profile_photo = models.ImageField(upload_to='static/', blank=True)
    bio = models.CharField(max_length=160, null=True, blank=True, default=None)
    gender = models.CharField(max_length=10, default=None, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True, default=None)
    age = models.IntegerField(null=True, blank=False)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(age__gte=18), name='is_adult')
        ]

class Follow(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='origin_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='destination_user')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_relationships',
                fields=['from_user', 'to_user']
            ),
            models.CheckConstraint(
                name='prevent_self_follow',
                check=~models.Q(from_user=models.F("to_user"))
            )
        ]
    
    def __str__(self):
        return f'{self.from_user.username} -> {self.to_user.username}'


class Post(models.Model):
    desc = models.CharField(max_length=250, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='static/', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post')
    likes = models.ManyToManyField(to='User', related_name='like')
    comments = models.ManyToManyField(to='Comment', related_name='comment')
    class Meta:
        ordering = ['posted_at']

    def __str__(self):
        return self.id


class Comment(models.Model):
    content = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id