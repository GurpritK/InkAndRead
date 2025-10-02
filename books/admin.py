from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Book


@admin.register(Book)
class MyModelAdmin(SummernoteModelAdmin):
    list_display = ('book_title', 'slug', 'author')
    search_fields = ['book_title', 'author']
    list_filter = ('book_title', 'average_rating')
    prepopulated_fields = {'slug': ('book_title',)}
    summernote_fields = ('content',)
