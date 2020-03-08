from django.test import TestCase

from catalog.models import Author, Book, Genre, Language


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'Died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1')


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified object used by all test methods
        author = Author.objects.create(first_name='Bik', last_name='Qerr')
        genre = Genre.objects.create(name='Eksperiment')
        language = Language.objects.create(name='Shqip')
        Book.objects.create(
            title='Trying test',
            author=author,
            summary='Duke testuar objektin/modelin Book. Duke praktikuar testet.',
            isbn='1111-222-33',
            language=language
        ).genre.set(Genre.objects.filter(id=1))

    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_language_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('language').verbose_name
        self.assertEqual(field_label, 'language')

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        # This will fail if the urlconf is not defined.
        self.assertEqual(book.get_absolute_url(), '/catalog/book/1')
