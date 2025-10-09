from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from books.models import Book
from .models import UserBookList


def index(request):
    """User profile page showing their book lists"""
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to view your profile.')
        return redirect('account_login')
    
    # Get user's book lists
    user_books = UserBookList.objects.filter(user=request.user)
    
    # Separate wishlist and read books
    favorite_books = user_books.filter(is_favorite=True).select_related('book')
    read_books = user_books.filter(is_read=True).select_related('book')
    
    # Get counts for stats
    favorites_count = favorite_books.count()
    read_count = read_books.count()
    total_books_count = Book.objects.count()
    
    context = {
        'favorite_books': favorite_books,
        'read_books': read_books,
        'favorites_count': favorites_count,
        'read_count': read_count,
        'total_books_count': total_books_count,
    }
    
    return render(request, 'user_profiles/profile.html', context)


def toggle_favorite(request, book_id):
    """Toggle wishlist status for a book"""
    if request.method != "POST":
        messages.error(request, 'Invalid request method.')
        return redirect('books')
    
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to add books to wishlist.')
        return redirect('account_login')
    
    book = get_object_or_404(Book, id=book_id)
    user_book, created = UserBookList.objects.get_or_create(
        user=request.user,
        book=book
    )
    
    # Toggle wishlist status
    user_book.is_favorite = not user_book.is_favorite
    user_book.save()
    
    # Show success message and redirect back
    action = 'added to' if user_book.is_favorite else 'removed from'
    messages.success(request, f'"{book.book_title}" {action} wishlist!')
    return redirect('book_detail', slug=book.slug)


def toggle_read(request, book_id):
    """Toggle read status for a book"""
    if request.method != "POST":
        messages.error(request, 'Invalid request method.')
        return redirect('books')
    
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to mark books as read.')
        return redirect('account_login')
    
    book = get_object_or_404(Book, id=book_id)
    user_book, created = UserBookList.objects.get_or_create(
        user=request.user,
        book=book
    )
    
    # Toggle read status
    user_book.is_read = not user_book.is_read
    user_book.save()
    
    # Show success message and redirect back
    action = 'marked as read' if user_book.is_read else 'marked as unread'
    messages.success(request, f'"{book.book_title}" {action}!')
    return redirect('book_detail', slug=book.slug)
