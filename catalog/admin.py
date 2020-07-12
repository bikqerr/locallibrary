from django.contrib import admin

from .models import Author, Genre, Book, Language, BookInstance, PublishHouse

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Language)
admin.site.register(PublishHouse)


admin.site.register(BookInstance)


# class BookInline(admin.TabularInline):
#     model = Book
#     fk_name = 'author'
#     extra = 0
#
#
# # Define the admin class
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
#     fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
#     inlines = 'author'
#
#     def get_authors(self):
#         return "\n".join([author.first_name for author in self.first_name.all()])
#
#
# # Register the admin class with the associated model
# admin.site.register(Author, AuthorAdmin)
#
#
# class BookInstanceInline(admin.TabularInline):
#     model = BookInstance
#     extra = 0
#
#
# # Register the Admin classes for Book using the decorator
# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'display_genre')
#     fields = [('isbn', 'title', 'covers_img', 'sub_title', 'original_title'), ('author', 'translate', 'curator'),
#               ('summary', 'genre', 'language', 'publishHouse', 'series')]
#     inlines = 'books'
#
#     def get_books(self):
#         books = []
#         for x in self.title.all():
#             books.append(x.title)
#         return books
#
#
# @admin.register(BookInstance)
# class BookInstance(admin.ModelAdmin):
#     list_display = ('book', 'status', 'borrower', 'due_back', 'id')
#     list_filter = ('status', 'due_back')
#
#     fieldsets = (
#         (None, {
#             'fields': ('book', 'imprint', 'id')
#         }),
#         ('Availability', {
#             'fields': ('status', 'due_back', 'borrower')
#         }),
#     )
