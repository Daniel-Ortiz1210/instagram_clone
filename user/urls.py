from django.urls import path
from .views import RegisterUser, UserProfile, Following, Followers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterUser.as_view(), name='register_user'),
    path('<username>/', UserProfile.as_view(), name='user_profile'),
    path('<username>/following/', Following.as_view(), name='following_list'),
    path('<username>/followers/', Followers.as_view(), name='followers_list')
]