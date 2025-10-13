# Entity Relationship Diagram (ERD) - Ink & Read Project

## Database Schema Overview

This ERD represents the complete database structure for the Ink & Read Django project, showing all models and their relationships.

```mermaid
erDiagram
    %% Django's built-in User model
    User {
        int id PK
        string username UK
        string email UK
        string password
    }

    %% Books app models
    Book {
        int id PK
        string book_title UK "max_length=200"
        string slug UK "max_length=200"
        text book_description
        string author "max_length=100"
        cloudinary_field cover_image "default=placeholder"
        string cover_image_alt "max_length=150"
    }

    BookRating {
        int id PK
        int user_id FK
        int book_id FK
        int score "1-5, validators"
        datetime created_at "auto_now_add=True"
        datetime updated_at "auto_now=True"
    }

    BookReview {
        int id PK
        int user_id FK
        int book_id FK
        text review
        datetime created_at "auto_now_add=True"
        datetime updated_at "auto_now=True"
        boolean approved "default=False"
    }

    %% User Profiles app models
    UserBookList {
        int id PK
        int user_id FK
        int book_id FK
        boolean is_favorite "default=False"
        boolean is_read "default=False"
        datetime date_added "auto_now_add=True"
        datetime date_updated "auto_now=True"
        text notes "nullable"
    }

    %% Relationships
    User ||--o{ BookRating : "rates"
    User ||--o{ BookReview : "reviews"
    User ||--o{ UserBookList : "manages_library"
    
    Book ||--o{ BookRating : "rated_by"
    Book ||--o{ BookReview : "reviewed_by"
    Book ||--o{ UserBookList : "in_user_lists"

    %% Unique constraints
    BookRating }|--|| User : "unique_together(user,book)"
    BookRating }|--|| Book : "unique_together(user,book)"
    
    BookReview }|--|| User : "unique_together(user,book)"
    BookReview }|--|| Book : "unique_together(user,book)"
    
    UserBookList }|--|| User : "unique_together(user,book)"
    UserBookList }|--|| Book : "unique_together(user,book)"
```

## Model Descriptions

### User (Django's Built-in)
- **Purpose**: Manages user authentication and basic profile information
- **Key Features**: Username, email, authentication fields
- **Relationships**: Central entity connected to all user-generated content

### Book
- **Purpose**: Stores book information including metadata and cover images
- **Key Features**: 
  - Unique title and slug for SEO-friendly URLs
  - Cloudinary integration for cover image storage
  - Author information and rich text descriptions
- **Methods**: `average_rating()`, `is_favorited_by()`, `is_read_by()`

### BookRating
- **Purpose**: Stores user ratings for books (1-5 stars)
- **Key Features**:
  - One rating per user per book (unique constraint)
  - Timestamp tracking for creation and updates
  - Validation for score range (1-5)
- **Related Name**: `ratings` (accessible via `book.ratings.all()`)

### BookReview
- **Purpose**: Stores detailed user reviews for books
- **Key Features**:
  - One review per user per book (unique constraint)
  - Admin approval system with `approved` flag
  - Rich text content support
- **Related Names**: `reviewer` (user), `reviewed_book` (book)

### UserBookList
- **Purpose**: Manages user's personal book library and reading status
- **Key Features**:
  - Favorite and read status tracking
  - Personal notes for each book
  - Timestamp tracking for library management
- **Related Names**: `book_lists` (user), `user_lists` (book)

## Key Relationships

1. **One-to-Many Relationships**:
   - User → BookRating (One user can rate many books)
   - User → BookReview (One user can review many books)
   - User → UserBookList (One user can have many books in library)
   - Book → BookRating (One book can have many ratings)
   - Book → BookReview (One book can have many reviews)
   - Book → UserBookList (One book can be in many user libraries)

2. **Unique Constraints**:
   - (User, Book) in BookRating: One rating per user per book
   - (User, Book) in BookReview: One review per user per book
   - (User, Book) in UserBookList: One library entry per user per book

## Database Indexes

- **Primary Keys**: Auto-generated `id` fields on all models
- **Unique Keys**: `book_title`, `slug` on Book; `username`, `email` on User
- **Foreign Keys**: All relationship fields create database indexes
- **Compound Indexes**: Unique constraints create compound indexes

## Business Logic Notes

- **Average Rating Calculation**: Computed dynamically via `Book.average_rating()` method
- **User Library Status**: Managed through boolean flags in `UserBookList`
- **Review Moderation**: Reviews require admin approval before display
- **Cascading Deletes**: User deletion removes all associated ratings, reviews, and library entries
- **Image Storage**: Cover images stored in Cloudinary with HTTPS enforcement