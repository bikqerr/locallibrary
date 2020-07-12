from django.db import models
# Used to generate URLs by reversing the URL patterns
from django.urls import reverse
# Required for unique book instance
import uuid
from django.contrib.auth.models import User
from datetime import date


class Genre(models.Model):
    """
    Model representing a book genre.
    """
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Language(models.Model):
    original = models.CharField(max_length=200, default='null')
    translatedIn = models.CharField(max_length=200, default='null', blank=True, null=True)

    def __str__(self):
        return 'Original: ' + self.original + ', Translated in: ' + self.translatedIn


class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}  {self.first_name}'


class ScanInventory(models.Model):
    """
    Info for tha scan process(work and payments).
    """


#     TODO Create this class


class PublishHouse(models.Model):
    """"""
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    covers_img = models.ImageField(upload_to='img/covers', default='/img/covers/defaultCoversImg.png')
    sub_title = models.CharField(max_length=500, null=True, blank=True)
    original_title = models.CharField(max_length=300, null=True, blank=True, default='null')

    # Foreign Key used because Book can have one author, but authors can have multiple books
    # Author as a string rather than a object because it hasn't been declared yet in the file
    author = models.ManyToManyField(Author, related_name='author', blank=True)
    translate = models.ManyToManyField(Author, related_name='translate', blank=True)
    curator = models.ManyToManyField(Author, related_name='curator', blank=True)
    summary = models.TextField(max_length=1000, help_text='Enter e brief description of the book', null=True,
                               blank=True)
    # From italian COLLANA
    series = models.CharField(max_length=300, null=True, blank=True)
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
    )

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book.', blank=True)
    language = models.ForeignKey('Language', on_delete=models.DO_NOTHING, null=True, blank=True, default='null')
    publishHouse = models.ManyToManyField(PublishHouse)

    def display_genre(self):
        """
        Create a string for Genre. This is required to display genre in Admin.
        """
        return ', '.join(genre.name for genre in self.genre.all())

    # the short description is the header of the returned table
    display_genre.short_description = 'Genre'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the url to acess a detail record for this book"""
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library.)
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text='Unique ID for this particular book across whole library'
    )
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reversed')
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        return f'{self.id} ({self.book.title})'
