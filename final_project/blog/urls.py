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
                  path('new/', views.new_Post, name='new_post'),
                  path('<int:pk>/', views.Post_Pre_View.as_view(), name='preview'),
                  path('register/', views.register, name='register'),
                  path('categories/', views.Categories.as_view(), name='categories'),
                  path('profile/<int:pk>/', views.Profile.as_view(), name='profile'),
                  path('likeapi/', views.likeAPI.as_view(), name='likeapi'),
                  path('likeapi/<int:pk>/', views.likeAPI.as_view(), name='likeapi'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
