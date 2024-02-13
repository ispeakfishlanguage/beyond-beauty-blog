from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('myposts/', views.UserPostsList.as_view(), name='user_posts'),
    path('mydrafts/', views.UserDraftsList.as_view(), name='user_drafts'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>/', views.PostLike.as_view(), name='post_like'),
    path(
        'comment/<int:comment_id>/edit/',
        views.CommentUpdate.as_view(),
        name='edit_comment'
    ),
    path(
        'comment/<int:comment_id>/delete/',
        views.CommentDelete.as_view(),
        name='delete_comment'),
    path('post/create/', views.PostCreate.as_view(), name='post_create'),
    path(
        'post/<int:pk>/update/',
        views.PostUpdate.as_view(),
        name='post-update'
    ),
    path(
        'post/<int:pk>/delete/',
        views.PostDelete.as_view(),
        name='post-delete'
    ),
]
