from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import BookRatingForm
from .models import Book

# Create your views here.


def index(request):
    """
    Display the home page.

    **Template:**
    :template:`books/index.html`
    """
    return render(request, 'books/index.html')


def books(request):
    """
    Display all books.

    **Context:**
    ``books``: List of all :model:`books.Book`

    **Template:**
    :template:`books/books.html`
    """

    books = Book.objects.all()
    return render(request, 'books/books.html', {'books': books})


def book_detail(request, slug):
    """
    Display an individual :model:`books.Book`.

    **Context**

    ``book``
        An instance of :model:`books.Book`.

    **Template:**

    :template:`books/book_detail.html`
    """

    book = get_object_or_404(Book, slug=slug)
    
    if request.method == "POST":
        book_rating_form = BookRatingForm(data=request.POST)
        if book_rating_form.is_valid():
            # Handle the rating using the separate method
            if handle_book_rating(request, book, book_rating_form):
                return redirect('book_detail', slug=slug)

    book_rating_form = BookRatingForm()
    
    # Get current user's rating if they're authenticated
    user_rating = get_user_rating(request.user, book)

    return render(
        request,
        "books/book_detail.html",
        {
            "book": book,
            "book_rating_form": book_rating_form,
            "user_rating": user_rating,
        },
    )


def get_user_rating(user, book):
    """
    Get the current user's rating for a specific book.
    
    **Parameters:**
    ``user``
        The user object
    ``book``
        The book instance
    
    **Returns:**
    ``BookRating`` or ``None``
        The user's rating if it exists, None otherwise
    """
    if user.is_authenticated:
        return book.ratings.filter(user=user).first()
    return None


def handle_book_rating(request, book, book_rating_form):
    """
    Handle the creation or update of a book rating.
    
    **Parameters:**
    ``request``
        The HTTP request object
    ``book``
        The book instance being rated
    ``book_rating_form``
        The validated rating form
    
    **Returns:**
    ``bool``
        True if rating was processed successfully, False otherwise
    """
    if not request.user.is_authenticated:
        messages.add_message(
            request, messages.ERROR,
            'You must be logged in to rate books.'
        )
        return False
    
    # Check if user already rated this book
    existing_rating = book.ratings.filter(user=request.user).first()
    
    try:
        if existing_rating:
            # Update existing rating
            existing_rating.score = book_rating_form.cleaned_data['score']
            existing_rating.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Your rating has been updated successfully!'
            )
        else:
            # Create new rating
            book_rating = book_rating_form.save(commit=False)
            book_rating.user = request.user
            book_rating.book = book
            book_rating.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Rating submitted successfully!'
            )
        return True
    except Exception:
        messages.add_message(
            request, messages.ERROR,
            'An error occurred while saving your rating. Please try again.'
        )
        return False
    

def delete_book_rating(request, book):
    """
    Delete a user's rating for a specific book.
    
    **Parameters:**
    ``request``
        The HTTP request object
    ``book``
        The book instance whose rating should be deleted
    
    **Returns:**
    ``bool``
        True if rating was deleted successfully, False otherwise
    """
    if not request.user.is_authenticated:
        messages.add_message(
            request, messages.ERROR,
            'You must be logged in to delete ratings.'
        )
        return False
    
    # Find the user's existing rating
    existing_rating = book.ratings.filter(user=request.user).first()
    
    if not existing_rating:
        messages.add_message(
            request, messages.WARNING,
            'No rating found to delete.'
        )
        return False
    
    try:
        existing_rating.delete()
        messages.add_message(
            request, messages.SUCCESS,
            'Your rating has been deleted successfully!'
        )
        return True
    except Exception:
        messages.add_message(
            request, messages.ERROR,
            'An error occurred while deleting your rating. Please try again.'
        )
        return False


def delete_rating_view(request, slug):
    """
    View to handle deletion of a book rating.
    
    **Parameters:**
    ``request``
        The HTTP request object
    ``slug``
        The book slug
    
    **Template:**
    Redirects to book detail page
    """
    book = get_object_or_404(Book, slug=slug)
    
    if request.method == "POST":
        if delete_book_rating(request, book):
            return redirect('book_detail', slug=slug)
        else:
            return redirect('book_detail', slug=slug)
    
    # If not POST, redirect to book detail
    return redirect('book_detail', slug=slug)
