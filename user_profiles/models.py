from django.db import models
from django.contrib.auth.models import User
from books.models import Book

# Create your models here.


class UserBookList(models.Model):
    """
    Stores user's favorite books and read status
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_lists')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='user_lists')
    is_favorite = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'book')
        ordering = ['-date_updated']
        verbose_name = 'User Book List'
        verbose_name_plural = 'User Book Lists'

    def __str__(self):
        status_parts = []
        if self.is_favorite:
            status_parts.append('Favorite')
        if self.is_read:
            status_parts.append('Read')
        
        status = ', '.join(status_parts) if status_parts else 'No status'
        return f"{self.user.username} - {self.book.book_title} ({status})"

    def get_display_status(self):
        """Get a friendly display of the book's status for templates"""
        status_parts = []
        if self.is_favorite:
            status_parts.append('❤️ Favorite')
        if self.is_read:
            status_parts.append('✅ Read')
        
        return status_parts if status_parts else ['📖 Added to library']
