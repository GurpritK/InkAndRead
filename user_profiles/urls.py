from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='profile'),
    path('toggle-favorite/<int:book_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('toggle-read/<int:book_id>/', views.toggle_read, name='toggle_read'),
]