from . import views
from .views import CommentUpdate, CommentDelete, PostCreate
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>/', views.PostLike.as_view(), name='post_like'),
    path('comment/<int:comment_id>/edit/', CommentUpdate.as_view(), name='edit_comment'),
    path('comment/<int:comment_id>/delete/', CommentDelete.as_view(), name='delete_comment'),
    path('post/create/', PostCreate.as_view(), name='post_create'),
]
