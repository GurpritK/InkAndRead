from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Book, BookRating


@admin.register(Book)
class BookAdmin(SummernoteModelAdmin):
    list_display = (
        'book_title', 'slug', 'author', 'average_rating', 'total_ratings'
    )
    search_fields = ['book_title', 'author']
    list_filter = ('author',)
    prepopulated_fields = {'slug': ('book_title',)}
    summernote_fields = ('book_description',)
    readonly_fields = ('average_rating', 'total_ratings')
    
    def total_ratings(self, obj):
        """Display total number of ratings for this book"""
        return obj.ratings.count()
    total_ratings.short_description = 'Total Ratings'


@admin.register(BookRating)
class BookRatingAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'score', 'created_at', 'updated_at')
    list_filter = ('score', 'created_at', 'updated_at', 'book__author')
    search_fields = ['book__book_title', 'user__username']
    list_editable = ('score',)
    date_hierarchy = 'created_at'
    list_per_page = 50
    
    fieldsets = (
        ('Rating Information', {
            'fields': ('user', 'book', 'score')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        """Optimize queries by selecting related objects"""
        return super().get_queryset(request).select_related('user', 'book')
