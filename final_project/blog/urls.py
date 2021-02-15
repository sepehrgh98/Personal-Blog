from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('new/', views.new_Post, name='new_post'),
    path('<int:pk>/', views.Post_Pre_View.as_view(), name='preview'),
]

app_name = 'blog'
