from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

'''
Prevent self-follow
https://adamj.eu/tech/2021/02/26/django-check-constraints-prevent-self-following/

'''

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    following = models.ManyToManyField(to='self', related_name='following_list', null=True, blank=True)
    followers = models.ManyToManyField(to='self', related_name='followers_list', null=True, blank=True)
    profile_photo = models.ImageField(upload_to='static/', blank=True)
    birthday = models.DateField(null=True, blank=True, default=None)
    bio = models.CharField(max_length=160, null=True, blank=True, default=None)
    gender = models.CharField(max_length=10, default=None, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(birthday__lte=(datetime.date.today() - datetime.timedelta(days=6570))), name='is_adult')
        ]


    def __str__(self):
        return self.username