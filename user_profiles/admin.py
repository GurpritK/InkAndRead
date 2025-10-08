from django.contrib import admin
from .models import UserBookList


@admin.register(UserBookList)
class UserBookListAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'is_favorite', 'is_read', 'date_added']
    list_filter = ['is_favorite', 'is_read', 'date_added']
    search_fields = ['user__username', 'book__book_title', 'book__author']
    readonly_fields = ['date_added', 'date_updated']
