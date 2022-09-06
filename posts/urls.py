from django.urls import path
from .views import CreatePostView, PostView, CommentsView

urlpatterns = [
    path('<username>/', CreatePostView.as_view()),
    path('<id>/', PostView.as_view()),
    path('<post_id>/comments/', CommentsView.as_view())
]