from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import View, FormView
from form_views import form_templates
from models import EludeUser, BookImage, Book, Watchlist, BookRentedOut, BookYouAreRenting, BookTradingOut
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
import search_algorithm
from variables import *
from django.template import RequestContext


current_search_state = None
redirect_page = None
class TextDoorHomePageView(View):

    def get(self, request):
        global current_search_state
        current_search_state = SEARCHING_FROM_HOME_PAGE
        return render(request, 'home_page.html', {'current_search_state': current_search_state})

class SignUpPageView(View):

    def get(self, request):
        global current_search_state
        current_search_state = None
        form = form_templates.UserSignUpForm()
        return render(request, 'sign_up_page.html', {'form': form})

    def post(self, request):
        form = form_templates.UserSignUpForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('user_name')
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User.objects.create_user(username=user_name, password=password, email=email, first_name=first_name,
                                            last_name=last_name)
            user.save()
            college_attending = form.cleaned_data['user_college']

            elude_user = EludeUser(username=user, college_attending=college_attending, new_user=True)
            elude_user.save()
            pk = elude_user.id
            if redirect_page == SEARCHING_FROM_HOME_PAGE:
                return HttpResponseRedirect(reverse('search_result_page',
                                                    kwargs={'pk':pk,'user_name':user_name}))
            return HttpResponseRedirect(reverse('user_home_profile_page',
                                                kwargs={'pk': pk, 'user_name': user_name}))
        else:
            return render(request, 'sign_up_page.html', {'form': form})


class UserHomeProfilePage(View):
    login_required = True

    def get(self, request, pk, user_name):
        first_name = User.objects.get(username=user_name)
        elude_user = EludeUser.objects.get(username=first_name)
        new_user = elude_user.new_user
        return render(request, 'user_profile_page.html', {'user_name':user_name, 'first_name':first_name, 'pk':pk,
                                                          'first_time_user': new_user})

    def post(self, request, pk, user_name):
        if request.POST.get("sign_out_button"):
            logout(request)
            return HttpResponseRedirect(reverse('login_page'))

class LoginView(FormView):

    form_class = form_templates.LogInForm
    template_name = 'log_in_page.html'

    def get_success_url(self):
        global current_search_state
        self.success_url = 'user_home_profile_page'
        first_name = User.objects.get(pk=self.request.user.id)
        elude_user = EludeUser.objects.get(username=first_name)
        elude_user.new_user = False
        elude_user.save()
        current_search_state = None
        return reverse(self.success_url, kwargs={'user_name': self.request.user.username, 'pk':self.request.user.id})

    def form_valid(self, form):
        name = form.cleaned_data['name']
        password = form.cleaned_data['password']
        user = authenticate(username=name, password=password)
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return render(self.request,'log_in_page.html', {'form': form})

class NewBookListingView(View):

    def get(self, request, user_name, pk):
        form = form_templates.RegisterBookForm()
        return render(request, 'new_book_entry.html', {'form': form, 'user_name': user_name, 'pk':pk})

    def post(self, request, user_name, pk):
        form = form_templates.RegisterBookForm(request.POST, request.FILES)
        if form.is_valid():
            name_of_book = form.cleaned_data.get('book_name')
            isbn_num = form.cleaned_data.get('isbn')
            author = form.cleaned_data.get('author')
            image_file = request.FILES['images']
            price = form.cleaned_data.get('price')
            book_condition = form.cleaned_data.get('book_condition')
            user = User.objects.get(username=user_name)
            new_book = Book(title=name_of_book, isbn_number=isbn_num, author=author, price=price,
                            book_condition=book_condition)
            if 'for_long_term_rent' in request.GET:
                new_book.long_term_rent = True
            else:
                new_book.long_term_rent = False
            if 'for_short_term_rent' in request.GET:
                new_book.short_term_rent = True
            else:
                new_book.short_term_rent = False
            if 'for_sale' in request.GET:
                new_book.for_buy = True
            else:
                new_book.for_buy = False
            if 'for_trade' in request.GET:
                new_book.for_trade = True
            else:
                new_book.for_trade = False
            new_book.book_owner = EludeUser.objects.get(username=user)
            new_book.save()
            book_image = BookImage(image_name=(name_of_book + " book image"), book_image=image_file, book=new_book)
            book_image.save()
            return HttpResponseRedirect(reverse('success_url_page', kwargs={'user_name': user_name, 'pk': pk}))
        else:
            return render(request, 'new_book_entry.html', {'form': form})

class SuccessPageView(View):
    def get(self, request, user_name, pk):
        return render(request, 'success_url.html', {'user_name':user_name, 'pk':pk})

class SearchView(View):

    def get(self, request, pk, user_name):
        query_string = ''
        found_entries = None
        global redirect_page
        if current_search_state == SEARCHING_FROM_HOME_PAGE:
            redirect_page = SEARCHING_FROM_HOME_PAGE
            guest_state = "true"
        else:
            guest_state = "false"
        if ('q' in request.GET) and request.GET['q'].strip():
            query_string = request.GET['q']

            entry_query = search_algorithm.get_query(query_string, ['title', 'isbn_number', 'author'])

            found_entries = Book.objects.filter(entry_query).order_by('publish_date')

            count = Book.objects.filter(entry_query).count()
        return render(request, 'search_results.html',
                          {'query_string': query_string, 'found_entries': found_entries, 'pk':pk,
                            'user_name':user_name, 'guess_state': guest_state, 'entry_query':count},
                          context_instance=RequestContext(request))
'''
    def post(self, request, pk, user_name):
        if self.request.POST.get('add_to_cart'):
            #create transaction_process object
'''


class ListOfYourBooksView(View):

    def get(self, request, pk, user_name):
        user = User.objects.get(username=user_name)
        elude_user = EludeUser.objects.get(username=user)
        user_book = Book.objects.filter(book_owner=elude_user)
        return render(request, 'all_user_books.html', {'user_book':user_book, 'pk':pk})

class SingleBookDescriptionView(View):

    def get(self, request, pk, book_id, slug):
        book = get_object_or_404(Book, slug=slug)
        book_image = BookImage.objects.filter(book=book).values()
        return render(request, 'book_discription_view.html', {'book':book, 'pk':pk, 'book_id':book_id,
                                                              'book_image': book_image})
    def post(self, request, pk, book_id, slug):

        if request.POST["watch-list"]:
            book = get_object_or_404(Book, slug=slug)
            elude_user = EludeUser.objects.get(username=request.user)
            if Watchlist.objects.filter(book=book, user=elude_user) is None:
                new_watch_list = Watchlist(book=book, user=elude_user)
                new_watch_list.save()
            return HttpResponseRedirect('')

class WatchListBooksView(View):

    def get(self, request, pk, user_name):
        user = User.objects.get(username=user_name)
        elude_user = EludeUser.objects.get(username=user)
        try:
            books = Watchlist.objects.filter(user=elude_user)
        except Watchlist.DoesNotExist:
            books = 'Start Watch List'
        return render(request, 'watch_list_books.html', {'books': books, 'pk':pk, 'elude_user':elude_user})
'''
class OrderHistoryView(View):

    def get(self, request, pk, user_name):
        user = User.objects.get(username=user_name)

'''
class BooksOutOnRentView(View):

    def get(self, request, pk, user_name):
        user = User.objects.get(username=user_name)
        elude_user = EludeUser.objects.get(username=user)
        try:
            books = BookRentedOut.objects.filter(user=elude_user)
        except BookRentedOut.DoesNotExist:
            books = None
        return render(request, 'books_out_on_rent.html', {'books':books, 'pk':pk, 'elude_user':elude_user})

class BooksYouAreRentingView(View):

    def get(self, request, pk, user_name):
        user = User.objects.get(username=user_name)
        elude_user = EludeUser.objects.get(username=user)
        try:
            books = BookYouAreRenting.objects.filter(user=elude_user)
        except BookYouAreRenting.DoesNotExist:
            books = None
        return render(request, 'book_you_are_renting.html', {'books':books, 'pk':pk, 'elude_user':elude_user})

class TradeHistoryView(View):

    def get(self, request, pk, user_name):
        user = User.objects.get(username=user_name)
        elude_user = EludeUser.objects.get(username=user)
        try:
            books = BookTradingOut.objects.filter(user=elude_user)
        except BookTradingOut.DoesNotExist:
            books = None
        return render(request, 'books_out_on_rent.html', {'books':books, 'pk':pk, 'elude_user':elude_user})



