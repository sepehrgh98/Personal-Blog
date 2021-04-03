from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'
urlpatterns = [
                  path(
                      'TagAPI/',
                      views.TagAutocomplete.as_view(),
                      name='Tag-autocomplete',
                  ),
                  path('', views.IndexView.as_view(), name='index'),
                  path('<int:pk>/', views.IndexView.as_view(), name='index'),
                  path('post/<int:pk>/', views.myPost.as_view(), name='post'),
                  path('new/', views.new_Post, name='new_post'),
                  path('register/', views.register, name='register'),
                  path('categories/', views.Categories.as_view(), name='categories'),
                  path('profile/<int:pk>/', views.Profile.as_view(), name='profile'),
                  path('likeapi/', views.likeAPI.as_view(), name='likeapi'),
                  path('likeapi/<int:pk>/', views.likeAPI.as_view(), name='likeapi'),
                  path('dislikeapi/', views.dislikeAPI.as_view(), name='dislikeapi'),
                  path('dislikeapi/<int:pk>/', views.dislikeAPI.as_view(), name='dislikeapi'),
                  path('LikeAndDislikeCountAPI/', views.LikeAndDislikeCountAPI.as_view(), name='like_dislike_count'),
                  path('LikeAndDislikeCountAPI/<int:pk>/', views.LikeAndDislikeCountAPI.as_view(),
                       name='like_dislike_count'),
                  path('UnlikeAPI/', views.UnlikeAPI.as_view(), name='UnlikeAPI'),
                  path('UnlikeAPI/<int:pk>/', views.UnlikeAPI.as_view(), name='UnlikeAPI'),
                  path('UndislikeAPI/', views.UndislikeAPI.as_view(), name='UndislikeAPI'),
                  path('UndislikeAPI/<int:pk>/', views.UndislikeAPI.as_view(), name='UndislikeAPI'),
                  path('CommentAPI/', views.CommentAPI.as_view(), name='CommentAPI'),
                  path('CommentAPI/<int:pk>/', views.CommentAPI.as_view(), name='CommentAPI'),
                path('CategoryAPI/', views.CategoryAPI.as_view(), name='CategoryAPI'),
                path('CategoryAPI/<string>/', views.CategoryAPI.as_view(), name='CategoryAPI'),
                  path('CategoryResultAPI/', views.CategoryResultAPI.as_view(), name='CategoryResultAPI'),
                  path('CategoryResultAPI/<string>/', views.CategoryResultAPI.as_view(), name='CategoryResultAPI'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
