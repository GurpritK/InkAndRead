from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # Landing page at root
    path('books/', views.books, name='books-list'),  # Books listing
    path('books/<slug:slug>/', views.book_detail, name='book_detail'),
    path(
        'books/<slug:slug>/delete-rating/',
        views.delete_rating_view,
        name='delete_rating'
    ),
]
