from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.IndexView.as_view(), name='index'),
                  path('new/', views.new_Post, name='new_post'),
                  path('<int:pk>/', views.Post_Pre_View.as_view(), name='preview'),
                  path('register', views.register, name='register'),
                  path('profile/<int:pk>/', views.Profile.as_view(), name='profile'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = 'blog'
