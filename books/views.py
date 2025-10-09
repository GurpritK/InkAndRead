from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import BookRatingForm, BookReviewForm
from .models import Book, BookReview

# Create your views here.


def index(request):
    """
    Display the home page.

    **Template:**
    :template:`books/index.html`
    """
    from datetime import datetime, timedelta
    from django.db.models import Avg, Count
    
    # Get current week's start (Monday)
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    
    # Try to get book with highest rating from this week
    book_of_week = None
    
    # First, try books rated this week
    books_this_week = Book.objects.filter(
        ratings__created_at__date__gte=week_start
    ).annotate(
        avg_rating=Avg('ratings__score'),
        rating_count=Count('ratings')
    ).filter(
        rating_count__gt=0  # Must have at least one rating
    ).order_by('-avg_rating', '-rating_count')
    
    if books_this_week.exists():
        book_of_week = books_this_week.first()
    else:
        # Fallback: get highest rated book overall
        all_books = Book.objects.annotate(
            avg_rating=Avg('ratings__score'),
            rating_count=Count('ratings')
        ).filter(
            rating_count__gt=0  # Must have at least one rating
        ).order_by('-avg_rating', '-rating_count')
        
        if all_books.exists():
            book_of_week = all_books.first()
    
    return render(request, 'books/index.html', {
        'book_of_week': book_of_week,
    })


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
        # Check which form was submitted
        if 'rating_submit' in request.POST:
            book_rating_form = BookRatingForm(data=request.POST)
            if book_rating_form.is_valid():
                # Handle the rating using the separate method
                if handle_book_rating(request, book, book_rating_form):
                    return redirect('book_detail', slug=slug)
        
        elif 'review_submit' in request.POST:
            book_review_form = BookReviewForm(data=request.POST)
            if book_review_form.is_valid():
                # Handle the review using the separate method
                if handle_book_review(request, book, book_review_form):
                    return redirect('book_detail', slug=slug)

    book_rating_form = BookRatingForm()
    book_review_form = BookReviewForm()
    
    # Get current user's rating if they're authenticated
    user_rating = get_user_rating(request.user, book)
    
    # Get current user's review if they're authenticated
    user_review = get_user_review(request.user, book)
    
    # Get user's favorite and read status
    user_book_status = get_user_book_status(request.user, book)
    
    # Get all approved reviews for this book
    approved_reviews = book.reviewed_book.filter(
        approved=True
    ).order_by('-created_at')

    return render(
        request,
        "books/book_detail.html",
        {
            "book": book,
            "book_rating_form": book_rating_form,
            "book_review_form": book_review_form,
            "user_rating": user_rating,
            "user_review": user_review,
            "user_book_status": user_book_status,
            "approved_reviews": approved_reviews,
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
        if not request.user.is_authenticated:
            messages.add_message(
                request, messages.ERROR,
                'You must be logged in to delete ratings.'
            )
        else:
            # Find the user's existing rating
            existing_rating = book.ratings.filter(user=request.user).first()
            
            if not existing_rating:
                messages.add_message(
                    request, messages.WARNING,
                    'No rating found to delete.'
                )
            else:
                try:
                    existing_rating.delete()
                    messages.add_message(
                        request, messages.SUCCESS,
                        'Your rating has been deleted successfully!'
                    )
                except Exception:
                    messages.add_message(
                        request, messages.ERROR,
                        'An error occurred while deleting your rating. '
                        'Please try again.'
                    )
    
    return redirect('book_detail', slug=slug)


def get_user_review(user, book):
    """
    Get the current user's review for a specific book.
    
    **Parameters:**
    ``user``
        The user object
    ``book``
        The book instance
    
    **Returns:**
    ``BookReview`` or ``None``
        The user's review if it exists, None otherwise
    """
    if user.is_authenticated:
        return book.reviewed_book.filter(user=user).first()
    return None


def handle_book_review(request, book, book_review_form):
    """
    Handle the creation or update of a book review.
    
    **Parameters:**
    ``request``
        The HTTP request object
    ``book``
        The book instance being reviewed
    ``book_review_form``
        The validated review form
    
    **Returns:**
    ``bool``
        True if review was processed successfully, False otherwise
    """
    if not request.user.is_authenticated:
        messages.add_message(
            request, messages.ERROR,
            'You must be logged in to write reviews.'
        )
        return False
    
    # Check if user already reviewed this book
    existing_review = book.reviewed_book.filter(user=request.user).first()
    
    try:
        if existing_review:
            # Update existing review (resets approval status)
            existing_review.review = book_review_form.cleaned_data['review']
            existing_review.approved = False  # Needs re-approval
            existing_review.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Your review has been updated and submitted for approval!'
            )
        else:
            # Create new review
            book_review = book_review_form.save(commit=False)
            book_review.user = request.user
            book_review.book = book
            book_review.approved = False  # Needs approval
            book_review.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Review submitted successfully! '
                'It will be visible after approval.'
            )
        return True
    except Exception:
        messages.add_message(
            request, messages.ERROR,
            'An error occurred while saving your review. Please try again.'
        )
        return False


def delete_review_view(request, slug):
    """
    View to handle deletion of a book review.
    
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
        if not request.user.is_authenticated:
            messages.add_message(
                request, messages.ERROR,
                'You must be logged in to delete reviews.'
            )
        else:
            # Find the user's existing review
            existing_review = book.reviewed_book.filter(
                user=request.user
            ).first()
            
            if not existing_review:
                messages.add_message(
                    request, messages.WARNING,
                    'No review found to delete.'
                )
            else:
                try:
                    existing_review.delete()
                    messages.add_message(
                        request, messages.SUCCESS,
                        'Your review has been deleted successfully!'
                    )
                except Exception:
                    messages.add_message(
                        request, messages.ERROR,
                        'An error occurred while deleting your review. '
                        'Please try again.'
                    )
    
    return redirect('book_detail', slug=slug)


def get_user_book_status(user, book):
    """
    Get the current user's favorite and read status for a specific book.
    
    **Parameters:**
    ``user``
        The user object
    ``book``
        The book instance
    
    **Returns:**
    ``UserBookList`` or ``None``
        The user's book status if it exists, None otherwise
    """
    if user.is_authenticated:
        return book.user_lists.filter(user=user).first()
    return None