from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book

# Create your views here.


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
    Display an individual :model:`book.Book`.

    **Context**

    ``post``
        An instance of :model:`book.Book`.

    **Template:**

    :template:`books/book_detail.html`
    """

    queryset = Book.objects.filter(status=1)
    books = get_object_or_404(queryset, slug=slug)

    return render(
        request,
        "book/book_detail.html",
        {"book": books},
    )
