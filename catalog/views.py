import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Book, Author, BookInstance, Genre, Language
from .forms import RenewBookForm, RenewBookModelForm


@login_required
def index(request):
    """
    View function for home page of site.
    """

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_books_contain_ja = Book.objects.filter(title__icontains='ja').count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    num_genre_start_p = Genre.objects.filter(name__istartswith='p').count()
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_books_contain_ja': num_books_contain_ja,
        'num_genre_start_p': num_genre_start_p,
        'num_visits': num_visits,
    }

    # Render the template index.html with the data in the contex variable
    return render(request, 'index.html', context=context)


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarians.
    """
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a Post request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    # your own name for the list as a template variable
    context_object_name = 'my_book_list'
    # Get all books containing the character a
    queryset = Book.objects.filter(title__icontains='a')
    # Specify your own template name/location
    template_name = 'catalog/my_template_name_list.html'
    paginate_by = 10


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user)\
            .filter(status__exact='o').order_by('due_back')


class BorrowedBooksForLiberianListView(PermissionRequiredMixin, generic.ListView):
    """
    Generic class-based view listing all books borrowed by all users.
    This view can be accessed only from users witch
    have the permission 'Set book as returned'
    """

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    permission_required = 'catalog.can_mark_returned'
    paginate_by = 10


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'my_author_list'
    # Get all authors
    queryset = Author.objects.all()
    template_name = 'catalog/all_author_list.html'
    paginate_by = 10


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '03/03/2020'}


class AuthorUpdate(UpdateView):
    model = Author
    fields = [
        'first_name',
        'last_name',
        'date_of_birth',
        'date_of_death'
    ]


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(CreateView):
    model = Book
    fields = '__all__'


class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
