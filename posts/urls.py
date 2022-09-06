from django.urls import path
from .views import CreatePostView, PostView

urlpatterns = [
    path('<username>/', CreatePostView.as_view()),
    path('<username>/<id>', PostView.as_view())
]