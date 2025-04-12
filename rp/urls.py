from django.urls import path
from . import views
urlpatterns = [
    path("",views.PostListView.as_view(),name="post-list"),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('#', views.LogoutView.as_view(), name='logout'),
    path("post-create/", views.PostCreateView.as_view(), name="post-create"),
    path('post-delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post-delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('profile/', views.ProfileDetailView.as_view(), name='view_profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('post-edit/<int:pk>/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:post_id>/add_comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('comment-edit/<int:pk>/', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('comment-delete/<int:pk>/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('user/<str:username>/', views.UserProfileView.as_view(), name='user_profile'),
    path('post/<int:pk>/like/', views.AddLikeView.as_view(), name='add_like'),
    path('post/<int:pk>/dislike/', views.AddDislikeView.as_view(), name='add_dislike'),
    path('comment/<int:pk>/like/', views.AddCommentLikeView.as_view(), name='add_comment_like'),
    path('comment/<int:pk>/dislike/', views.AddCommentDislikeView.as_view(), name='add_comment_dislike'),
    path('post/<int:post_id>/add_comment/', views.AddCommentView.as_view(), name='add_comment'),

]









    


