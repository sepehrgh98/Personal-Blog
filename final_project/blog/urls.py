from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('new/', views.new_Post, name='new_post'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]
