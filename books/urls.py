from django.urls import path
from . import views

urlpatterns = [
    path('', views.books, name='books-list'),
    path('<slug:slug>/', views.book_detail, name='book_detail'),
]
