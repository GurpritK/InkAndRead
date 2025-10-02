from django.db import models
from cloudinary.models import CloudinaryField


class Book(models.Model): 
    book_title = models.CharField(max_length=200, unique=True) 
    slug = models.SlugField(max_length=200, unique=True) 
    book_description = models.TextField()
    # author = models.ForeignKey(OtherModel, on_delete=models.CASCADE, related_name="other-app_other-model-items" ) 
    author = models.CharField(max_length=100)
    average_rating = models.FloatField()
    cover_image = CloudinaryField('image', default='placeholder')
    cover_image_alt = models.CharField(max_length=150)

    def __str__(self):
        return self.book_title
