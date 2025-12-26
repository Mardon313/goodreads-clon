from django.contrib import admin
from books.models import Book,Author,BookAuthor,BookReview

class BookAdmin(admin.ModelAdmin):
    search_fields = ['title','isbn']
    list_display = ['title','isbn','description']

class AutherAdmin(admin.ModelAdmin):
    pass

class BookAutherAdmin(admin.ModelAdmin):
    pass

class BookReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AutherAdmin)
admin.site.register(BookAuthor, BookAutherAdmin)
admin.site.register(BookReview, BookReviewAdmin)

