from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField


class Book(models.Model):
    """
    Stores a single book entry with details about the book and it's cover image
    """
    book_title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    book_description = models.TextField()
    author = models.CharField(max_length=100)
    cover_image = CloudinaryField('image', default='placeholder')
    cover_image_alt = models.CharField(max_length=150)

    # class Meta:
    #     ordering = [""]

    def __str__(self):
        return self.book_title
   
    def average_rating(self):
        qs = self.ratings.all()
        return round(qs.aggregate(models.Avg('score'))['score__avg'] or 0, 2)


class BookRating(models.Model):
    """
    Stores a single book rating per user per book
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'book')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} → {self.book.book_title}: {self.score}"
