from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import View, FormView
from form_views import form_templates
from models import EludeUser, BookImage, Book, Watchlist,\
    EludeUserAddress, StripeData, PaymentCardData, SoldBooks, BooksStudentsRequested, StudentFeedBacks
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
import search_algorithm
from django.template import RequestContext
import variables
from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from braces.views import LoginRequiredMixin
import isbnlib
from helper_functions import get_string_from_list, stripe_token, get_activation_code, generate_invoice_number, \
    get_buyers_fee, get_total_price_of_purchase, convert_str_to_money, get_textdoar_commission
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import string
import stripe
from helper_functions import application_fee_amount
from elude_web_application.setting_secret import TEST_STRIPE_API_KEY, STRIPE_LIVE_SECRET_KEY, STRIPE_LIVE_PUBLISHABLE_KEY
from django.contrib import messages
import os, stat
from delete_isbn_pic_dir import DELETE_PIC_DIR
from templated_email import send_templated_mail
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
# global variables used throughout user's logged in time

book_image_list_for_search = []
dictionary = []


class TextDoorHomePageView(View):

    def get(self, request):
        if request.user.is_authenticated():
            user_name = request.user.username
        else:
            user_name = "guest"
        return render(request, 'home_page.html', {'user_name': user_name})


class SignUpPageView(View):

    def get(self, request):
        form = form_templates.UserSignUpForm()
        return render(request, 'sign_up_page.html', {'form': form, 'user_name': "guest"})

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
            user.is_active = False
            user.save()
            college_attending = form.cleaned_data['user_college']
            elude_user = EludeUser(username=user, college_attending=college_attending, new_user=True)
            elude_user.save()
            activation_code = get_activation_code()
            send_templated_mail(
                template_name='activation_email',
                from_email='no reply',
                recipient_list=['email@textdoar.com', email],
                context={
                    'activation_code': activation_code,
                     'user_name': elude_user.username.username,
                    'first_name': elude_user.username.first_name
                },
                bcc=[variables.CUSTOMER_SERVICE_EMAIL],
                headers={'My-Custom-Header':'Textdoar Team'},
            )
            self.request.session['user_name'] = user_name
            self.request.session['email_name'] = email
            self.request.session['first_name'] = elude_user.username.first_name
            return HttpResponseRedirect(reverse('user_activation_page',
                                                    kwargs={'user_name': user_name}))
        else:
            return render(request, 'sign_up_page.html', {'form': form})


class UserHomeProfilePage(LoginRequiredMixin, View):

    def get(self, request, user_name):
        elude_user = EludeUser.objects.get(username=request.user)
        try:
            self.request.session.get("first_time_user")
            first_time_user = "True"
            del self.request.session['first_time_user']
        except(TypeError, KeyError, None):
            first_time_user = None

        return render(request, 'user_profile_page.html', {'user_name': elude_user.username.username,
                                                          'first_name': elude_user.username.first_name,
                                                          'first_time_user': first_time_user})

    def post(self, request, user_name):
        logout(request)
        return HttpResponseRedirect(reverse('logout'))


class SellingInformationView(View):
    def get(self, request):
        if request.user.is_authenticated():
            user_name = request.user.username
        else:
            user_name = "guest"
        return render(request, 'selling_a_textbook_info_page.html', {'user_name':user_name})


class BuyingInformationView(View):
    def get(self, request):
        if request.user.is_authenticated():
            user_name = request.user.username
        else:
            user_name = "guest"
        return render(request, 'buying_a_textbook_info_page.html', {'user_name': user_name})


class FAQView(View):
    def get(self, request):
        if request.user.is_authenticated():
            user_name = request.user.username
        else:
            user_name = "guest"
        return render(request, 'faq_page.html', {'user_name':user_name})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return render(request, 'home_page.html', {'user_name': "guest"})


class LoginViews(FormView):

    form_class = form_templates.LogInForm
    template_name = 'log_in_page.html'

    def get_success_url(self):
        elude_user = EludeUser.objects.get(username=self.request.user)
        elude_user.save()
        try:
            url_with_get = self.request.POST.get('next', None)
        except:
            url_with_get = None
        if url_with_get and (self.request.user.username in url_with_get or "guest" in url_with_get or
                                 'payment-signup-confirmation' in url_with_get):
            if "guest" in url_with_get:
                url_with_get = string.replace(url_with_get, "guest",self.request.user.username)
            redirect_to = url_with_get
            redirect_to = (redirect_to if is_safe_url(redirect_to, self.request.get_host())
                   else '/')
            return redirect_to
        return reverse('user_home_profile_page', kwargs={'user_name': self.request.user.username})

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        password = form.cleaned_data.get('password')
        user = authenticate(username=name, password=password)
        try:
            elude_user = EludeUser.objects.get(username=User.objects.get(username=name))
        except EludeUser.DoesNotExist:
            elude_user = None
            user = None
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponseRedirect(self.get_success_url())
            else:
                elude_user = elude_user.username
                self.request.session['user_name'] = elude_user.username
                self.request.session['email_name'] = elude_user.email
                self.request.session['first_name'] = elude_user.first_name
                return HttpResponseRedirect(reverse('user_activation_page',
                                                    kwargs={'user_name': elude_user.username}))
        else:
            return render(self.request,'log_in_page.html', {'form': form})

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(LoginViews, self).get_context_data(**kwargs)
        try:
            context['user_name'] = self.request.user.username
        except (None, TypeError, KeyError):
            context['user_name'] = "guest"
        return context


class AccountActivationView(View):

    def get(self, request, user_name):
        form = form_templates.ActivateAccountForm()
        # takes care of people that accidentally stumble across this url since its not login protected.
        try:
            user_name = self.request.session['user_name']
            user_email = self.request.session['email_name']
        except(KeyError, TypeError, None):
            return HttpResponseRedirect(reverse('user_registration_page'))
        return render(request, 'activate_account_form.html', {'user_name': user_name, 'form':form, 'user_email':user_email})

    def post(self, request, user_name):
        form = form_templates.ActivateAccountForm(request.POST)
        user_name = self.request.session['user_name']
        user_email = self.request.session['email_name']
        first_name = self.request.session['first_name']
        if request.POST.get("generate-new-code"):
            activation_code = get_activation_code()
            send_templated_mail(
                template_name='activation_email',
                from_email='Textdoar Team',
                recipient_list=['email@textdoar.com', user_email],
                context={
                    'activation_code': activation_code,
                     'first_name': first_name,
                },
                bcc=[variables.CUSTOMER_SERVICE_EMAIL],
            )
            messages.success(request, 'Sent Code!')
            return render(request, 'activate_account_form.html', {'form': form, 'new_code_generation':"True",
                                                                  'user_email':user_email})
        if request.POST.get("activate-account"):
            if form.is_valid():
                user = User.objects.get(username=user_name)
                user.is_active = True
                user.save()
                self.request.session['first_time_user'] = "True"
                send_templated_mail(
                template_name = 'welcome_email',
                from_email = 'Textdoar Team',
                recipient_list = ['email@textdoar.com', user_email],
                context={
                    'user_name': user.username,
                     'first_name': first_name,
                },
                bcc=[variables.CUSTOMER_SERVICE_EMAIL],
                )
                messages.success(request, 'Sent Code!')
                return HttpResponseRedirect(reverse('login_page'))
            else:
                return render(request, 'activate_account_form.html', {'form': form, 'user_email':user_email})


class ISBNView(View):

    def get(self, request, user_name):
        if request.user.is_authenticated():
            user_name = request.user.username
        else:
            user_name = "guest"
        return render(request, 'isbn_entry.html', {'user_name': user_name})

    def post(self, request, user_name):
        error = False
        if request.POST.get("search_value"):
            value = request.POST.get("isbn_value")
            # check if user entered something
            if value.strip():
                try:
                    isbn_from_word = isbnlib.isbn_from_words(value)
                except:
                    isbn_from_word = False
                    error = True
                if isbn_from_word:
                    try:
                        check_isbn_exist = (isbnlib.is_isbn10(isbn_from_word) or isbnlib.is_isbn13(isbn_from_word))
                    except:
                        check_isbn_exist = False
                        error = True
                    if check_isbn_exist:
                        try:
                            isbn_to_book_info = isbnlib.meta(isbn_from_word, service='default', cache='default')
                        except None:
                            isbn_to_book_info = None
                            error = True
                        if isbn_to_book_info:
                            isbn_author = get_string_from_list(isbn_to_book_info['Authors'])
                            isbn_title = isbn_to_book_info['Title']
                            isbn_isbn = isbn_to_book_info['ISBN-13']
                        else:
                            isbn_author = None
                            isbn_title = None
                            isbn_isbn = None
                            error = True
                        try:
                            isbn_picture_tuple = isbnlib.cover(isbn_from_word)
                            isbn_picture = isbn_picture_tuple[0]
                            isbn_downloaded_pic = isbn_picture_tuple[1]
                        except (TypeError, KeyError, OSError):
                            isbn_picture = None
                            isbn_downloaded_pic = "No Image Given"
                        try:
                            os.chmod(DELETE_PIC_DIR + '/' + isbn_downloaded_pic, stat.S_IWRITE)
                            os.remove(DELETE_PIC_DIR + '/' + isbn_downloaded_pic)
                        except(TypeError, KeyError, OSError):
                            pass

                        dictionary = {'isbn_author': isbn_author, 'isbn_title':isbn_title,
                                      'isbn_isbn': isbn_isbn, 'isbn_picture':isbn_picture,
                                      'isbn_picture_name': isbn_downloaded_pic}

                        self.request.session['dictionary'] = dictionary

                        return render(request, 'isbn_entry.html', {'user_name': self.request.user.username,
                                                  'isbn_from_word' : isbn_from_word, 'isbn_author': isbn_author, 'isbn_title':
                                                           isbn_title, 'value':value, 'isbn_isbn':isbn_isbn,
                                                           'isbn_picture': isbn_picture, 'check_isbn_exist':
                                                                   check_isbn_exist,
                                                                   'isbn_to_book_info': isbn_to_book_info, 'error':error})
                    else:
                        return render(request, 'isbn_entry.html', {'user_name': self.request.user.username,
                                                               'value': value, 'error':error})
                else:
                    return render(request, 'isbn_entry.html', {'user_name': self.request.user.username, 'value': value,
                                                           'error':error})
            else:
                return render(request, 'isbn_entry.html', {'user_name': self.request.user.username, 'value': value,
                                                           'error':error})
        if request.POST.get("finalizing_list"):
            try:
                self.request.session.get('dictionary', False)
            except (KeyError, TypeError):
                return HttpResponseRedirect(reverse('new_book_entry_page',
                                                        kwargs={'user_name':self.request.user.username}))

            return HttpResponseRedirect(reverse('new_book_entry_page', kwargs={'user_name': self.request.user.username}))
        if request.POST.get("manually_list"):
            return HttpResponseRedirect(reverse('new_book_entry_page',
                                                    kwargs={'user_name': self.request.user.username}))


class NewBookListingView(LoginRequiredMixin, View):

    def get(self, request, user_name):
        if request.user.is_authenticated():
            user_name = self.request.user.username
        else:
            user_name = "guest"
        try:
            dictionary_new = self.request.session.get('dictionary', False)
        except (KeyError, TypeError):
            return HttpResponseRedirect(reverse('isbn_entry_page', kwargs={'user_name':user_name}))
        try:
            form = form_templates.RegisterBookForm(initial={'book_name':dictionary_new['isbn_title'],
                                                            'author':dictionary_new['isbn_author'],
                                                            'isbn':dictionary_new['isbn_isbn'],
                                                            })
        except (KeyError, TypeError):
            form = form_templates.RegisterBookForm()
        return render(request, 'new_book_entry.html', {'form': form, 'user_name': self.request.user.username})

    def post(self, request, user_name):
        form = form_templates.RegisterBookForm(request.POST, request.FILES)
        if form.is_valid():
            ''' #comback to this later giving users the ability to pre-post
            if self.request.POST.get('date_specified_check'):
                pub_date = self.request.POST.get("inputed_date")
                pub_date_clean = datetime.strptime(pub_date, '%Y-%m-%d')
                publish_type = variables.SPECIFIC_DATE
            elif self.request.POST.get('end_of_the_semester'):
                date_format = "%Y-%m-%d"
                pub_date_clean = variables.KANSAS_STATE_UNIVERSITY_END_OF_SEMESTER_DATE
                pub_date_clean.strftime(date_format)
                publish_type = variables.END_OF_SEMESTER
            else:
                date_format = "%Y-%m-%d"
                pub_date_clean = datetime.today()
                pub_date_clean.strftime(date_format)
                publish_type = variables.NOW
                '''
            date_format = "%Y-%m-%d"
            pub_date_clean = datetime.today()
            pub_date_clean.strftime(date_format)
            publish_type = variables.NOW
            elude_user = EludeUser.objects.get(username=request.user)
            name_of_book = form.cleaned_data.get('book_name')
            isbn_num = form.cleaned_data.get('isbn')
            author = form.cleaned_data.get('author')
            image_file = request.FILES.get('images', False)
            book_condition = form.cleaned_data.get('book_condition')
            book_price = form.cleaned_data.get('book_price')
            book_edition = form.cleaned_data.get('book_edition')
            book_description = form.cleaned_data.get('book_description')
            try:
                edit_mode = self.request.session.get('edit_mode')
            except(KeyError, TypeError, None):
                edit_mode = None
            if edit_mode:
                edit_book = Book.objects.get(id=edit_mode)
                edit_book.author = author
                edit_book.title = name_of_book
                edit_book.book_condition = book_condition
                edit_book.book_description = book_description
                edit_book.publish_date = pub_date_clean
                edit_book.publish_type = publish_type
                edit_book.sales_price = book_price
                edit_book.isbn_number = isbn_num
                edit_book.save()
            else:
                new_book = Book(title=name_of_book, isbn_number=isbn_num, author=author,
                            book_condition=book_condition,
                            sales_price=book_price,
                            book_edition=book_edition,
                            book_description=book_description, book_owner=elude_user,
                            publish_date=pub_date_clean,
                            publish_type=publish_type)
                new_book.save()
            if image_file:
                if edit_mode:
                    new_book = Book.objects.get(id=edit_mode)
                    try:
                        book_old_image = BookImage.objects.get(book=new_book)
                        book_old_image.delete()
                    except:
                        pass
                    book_image = BookImage(image_name=(name_of_book + " book image"), book_image=image_file, book=new_book)
                    book_image.save()
                else:
                    book_image = BookImage(image_name=(name_of_book + " book image"), book_image=image_file, book=new_book)
                    book_image.save()
            else:
                dictionary_new = self.request.session.get('dictionary', False)
                try:
                    image_url = dictionary_new['isbn_picture']
                except (TypeError, KeyError, None):
                    image_url = None
                    image_file = None
                if image_url: # new book listing entry
                    r = requests.get(image_url)
                    image = NamedTemporaryFile(delete=True)
                    image.write(r.content)
                    image.flush()
                    image_file = File(image)
                    image_file.name = dictionary_new['isbn_picture_name']
                    book_image = BookImage(image_name=(name_of_book + " book image"), book_image=image_file, book=new_book)
                    book_image.save()
            user = EludeUser.objects.get(username=self.request.user)
            if user.address.count() is 0:
                if not user.stripe_account_activated:
                    self.request.session['redirect_to_stripe_listing_page'] = "True"
                return HttpResponseRedirect(reverse('address_entry_page', kwargs={'user_name':user_name}))
            if not user.stripe_account_activated:
                return HttpResponseRedirect(reverse('list_book_confirmation_page', kwargs={'user_name': user_name}))
            if edit_mode:
                del self.request.session['edit_mode']
                return HttpResponseRedirect(reverse('list_of_your_books', kwargs={'user_name':user_name}))

            send_templated_mail(
                template_name='new_book_listed',
                from_email='no reply',
                recipient_list=['email@textdoar.com', elude_user.username.email],
                context={
                    'book': new_book.title,
                     'isbn_number': new_book.isbn_number,
                    'first_name': elude_user.username.first_name,
                    'price': new_book.sales_price,
                    'textdoar_commission': get_textdoar_commission(new_book.sales_price),
                    'book_condition': new_book.book_condition,
                    'book_edition': new_book.book_edition,
                },
                bcc=[variables.CUSTOMER_SERVICE_EMAIL],
            )
            self.request.session['new_message'] = variables.REGISTERED_NEW_BOOK
            return HttpResponseRedirect(reverse('success_url_page', kwargs={'user_name': user_name}))
        else:
            return render(request, 'new_book_entry.html', {'form': form})


class SuccessPageView(View):

    def get(self, request, user_name):
        try:
            message_success = self.request.session.get('new_message')
        except (KeyError, TypeError, None):
            message_success = False
        return render(request, 'success_url.html', {'user_name':self.request.user.username, 'message': message_success})


class CartView(LoginRequiredMixin, View):
    def get(self, request, user_name):
        try:
            shopping_cart = self.request.session.get('shopping_cart')
        except (KeyError, TypeError, None):
            shopping_cart = None
        if shopping_cart:
            cart = []
            total_order = 0
            total_order_with_tax = 0
            elude_user = EludeUser.objects.get(username=request.user)
            if elude_user.address.count() is 0 or elude_user.address.all().filter(current_shipping_address=True).count() is 0:
                self.request.session['redirect_to_payment_page'] = 'True'
                has_address = False
            else:
                has_address = True
            delivery_time = datetime.now() + timedelta(hours=24)
            delivery_time = delivery_time.strftime("%A %d. %B %Y")
            if shopping_cart is not None:

                for item in shopping_cart:
                        book = get_object_or_404(Book, id=item)
                        cart.append(book)
                        total_order += float(book.sales_price)
                        total_order_with_tax += float(get_total_price_of_purchase(book.sales_price))


            self.request.session['total_order_price'] = total_order
            if elude_user.payment_card_info.count() > 0:
                try:
                    payment_data = elude_user.payment_card_info.all().filter(is_user_current_option=True)
                except (TypeError, KeyError, None):
                    payment_data = None
                if payment_data:
                    payment_saved = True
                else:
                    payment_saved = False
            else:
                payment_saved = False
            total_order = convert_str_to_money(str(total_order))
            total_order_with_tax = convert_str_to_money(str(total_order_with_tax))
            return render(request, 'cart.html', {'cart': cart,'user_name': user_name,
                                             'has_address': has_address, 'delivery_time':delivery_time, 'total_order':
                                             total_order, 'payment_saved':payment_saved, 'total_order_with_tax':
                                                 total_order_with_tax,'shopping_cart':shopping_cart})
        else:
            return render(request, 'cart.html', {'cart':None})

    def post(self, request, user_name):
        dynamic_cart = self.request.session.get('shopping_cart')
        if 'remove-book' in request.POST:
            book_id = request.POST.get("remove-book")
            del dynamic_cart[book_id]
            self.request.session['shopping_cart'] = dynamic_cart
            return HttpResponseRedirect('')
        return HttpResponseRedirect('')


class SearchResultView(View):

    def get(self, request, user_name):
        book_image_list_for_search = []
        form = form_templates.BooksStudentNeedForm()
        if not request.user.is_authenticated():
            user_name = "guest"
        else:
            user_name = self.request.user.username
        delivery_time = datetime.now() + timedelta(hours=36)
        delivery_time = delivery_time.strftime("%A %d. %B %Y")
        if 'q' in request.GET and request.GET['q'].strip():
            query_string = str(request.GET['q'])
            entry_query = search_algorithm.get_query(query_string, ['title', 'isbn_number', 'author'])
            try:
                elude_user = EludeUser.objects.get(username=request.user)
                found_entries = Book.objects.filter(entry_query).filter(~Q(book_owner=elude_user)).filter(book_is_sold=False).order_by('publish_date')
            except:
                found_entries = Book.objects.filter(entry_query).filter(book_is_sold=False).order_by('publish_date')
            if found_entries:
                for book in found_entries:
                    if book.book_owner.stripe_account_activated and book.book_owner.address.count() > 0:
                        book_image = BookImage.objects.filter(book=book).values()
                        book_image_list_for_search.append((book, book_image))
                return render(request, 'search_results.html', {'query_string': query_string, 'found_entries': found_entries,
                                                       'user_name': user_name, 'form':form,
                                                        'list_of_book_image':
                                                           book_image_list_for_search, 'delivery_time': delivery_time},
                                                                context_instance=RequestContext(request))

            return render(request, 'search_results.html', {'found_entries': None, 'form':form,
                                                           'query_string':query_string, 'user_name':user_name})
        return render(request, 'search_results.html', {'no_found_entries': True, 'user_name':user_name})

    def post(self, request, user_name):
        form = form_templates.BooksStudentNeedForm(request.POST)
        if form.is_valid():
            isbn_number = form.cleaned_data.get("isbn_number")
            email = form.cleaned_data.get("email")
            name_of_book = form.cleaned_data.get("name_of_book")
            new_book_request = BooksStudentsRequested(isbn_number=isbn_number, email=email, name_of_book=name_of_book)
            new_book_request.save()
            email = EmailMessage(variables.BOUGHT_BOOK_MESSAGE_EMAIL_SUBJECT,
                                 "We Hope to let you when it comes in in the next week",
                                 variables.TEXTDOAR_EMAIL, ['Uzzije2000@yahoo.co.uk'])
            email.send()
            self.request.session['new_message'] = "You Just Successfully Notified Us"
            return HttpResponseRedirect(reverse('success_url_page', kwargs={'user_name':self.request.user.username}))
        else:
            return render(request, 'search_results.html', {'form': form})


class ListOfYourBooksView(LoginRequiredMixin, View):

    def get(self, request, user_name):
        user_books = []
        user = User.objects.get(username=request.user)
        elude_user = EludeUser.objects.get(username=user)
        user_book = Book.objects.filter(book_owner=elude_user).filter(book_is_sold=False)
        for book in user_book:
                book_image = BookImage.objects.filter(book=book).values()
                user_books.append((book, book_image))
        return render(request, 'all_user_books.html', {'user_book': user_books})

    def post(self, request, user_name):
        if 'edit-book-id' in request.POST:
            book_id = request.POST.get("edit-book-id")
            edit_book = Book.objects.get(id=book_id)
            form = form_templates.RegisterBookForm(initial={'book_name':edit_book.title,
                                                            'author':edit_book.author,
                                                            'isbn':edit_book.isbn_number,
                                                            'book_condition': edit_book.book_condition,
                                                            'book_edition': edit_book.book_edition,
                                                            'book_price': edit_book.sales_price,
                                                            'book_description': edit_book.book_description,
                                                            })
            self.request.session['edit_mode'] = book_id
            return render(request, 'new_book_entry.html', {'form':form, 'user_name':self.request.user.username,
                                                         'edit_book_form':'True'})

        if 'delete-book-id' in request.POST:
            book_id = request.POST.get("delete-book-id")
            delete_book = Book.objects.get(id=book_id)
            messages.success(request, 'Sweet! %s was deleted!'% delete_book.title)
            delete_book.delete()
            return HttpResponseRedirect('')


class SingleBookDescriptionView(LoginRequiredMixin, View):

    def get(self, request, book_id, slug):
        if not request.user.is_authenticated():
            user_name = "guest"
        else:
            user_name = self.request.user.username
        book = get_object_or_404(Book, id=book_id)
        book_image = BookImage.objects.filter(book=book).values()
        return render(request, 'book_discription_view.html', {'book':book,'book_id':book_id,
                                                                'book_image': book_image,
                                                              'user_name': user_name,
                                                              })

    def post(self, request, book_id, slug):
        book = get_object_or_404(Book, id=book_id)
        book_image = BookImage.objects.filter(book=book).values()
        if 'watch-list' in request.POST:
            book = get_object_or_404(Book, id=book_id)
            elude_user = EludeUser.objects.get(username=request.user)
            try:
                no_entry = Watchlist.objects.get(book=book, user=elude_user)
            except Watchlist.DoesNotExist:
                no_entry = None
            if no_entry is None:
                new_watch_list = Watchlist(book=book, user=elude_user)
                new_watch_list.save()
                messages.success(request, 'Added to watchlist!')
            return HttpResponseRedirect('')

        if 'add_to_cart' in request.POST:
            shopping_cart_lists = self.request.session.get('shopping_cart')
            if shopping_cart_lists is None:
                shopping_cart_lists = {book_id:book_id}
            elif book_id not in shopping_cart_lists:
                shopping_cart_lists[book_id] = book_id
            self.request.session['shopping_cart'] = shopping_cart_lists
            messages.success(request, 'Added to cart! Click cart to checkout.')
            return HttpResponseRedirect('')


class WatchListBooksView(LoginRequiredMixin, View):

    def get(self, request, user_name):
        watch_list_books_list = []
        if not request.user.is_authenticated():
            user_name = "guest"
        else:
            user_name = self.request.user.username
        user = User.objects.get(username=request.user.username)
        elude_user = EludeUser.objects.get(username=user)
        try:
            watch_list_books = Watchlist.objects.filter(user=elude_user)
        except Watchlist.DoesNotExist:
            watch_list_books = None
        if watch_list_books:
            for book in watch_list_books:
                    book_image = BookImage.objects.filter(book=book.book).values()
                    watch_list_books_list.append((book, book_image))
        return render(request, 'watch_list_books.html', {'watch_list_books_list': watch_list_books_list, 'user_name': user_name})

    def post(self, request, user_name):
        if 'delete-book-id' in request.POST:
            book_id_for_deletion = str(self.request.POST.get("delete-book-id"))
            book = Book.objects.get(pk=book_id_for_deletion)
            Watchlist.objects.get(book=book).delete()
            return HttpResponseRedirect('')


class AddressView(LoginRequiredMixin, View):
    def get(self, request, user_name):
        elude_user = EludeUser.objects.get(username=self.request.user)
        if elude_user.address.count() is 0:
            pop_up_address_form = "True"
            addresses = None
        else:
            pop_up_address_form = "False"
            addresses = elude_user.address.all()
        form = form_templates.AddressBookForm()
        return render(request, 'address_page.html', {'form': form, 'user_name': elude_user.username.username,
                                                     'pop_up_address_form': pop_up_address_form, 'addresses':addresses})

    def post(self, request, user_name):
        global message
        form = form_templates.AddressBookForm(request.POST)
        eludeuser = EludeUser.objects.get(username=self.request.user)
        if 'edit-address' in request.POST:
            address_id = request.POST.get("edit-address")
            edit_address = EludeUserAddress.objects.get(id=address_id)
            form = form_templates.AddressBookForm(initial={'address':edit_address.address,'city':edit_address.city,
                                                           'zip_code':edit_address.zip_code,'state':edit_address.state})
            addresses = eludeuser.address.all()
            self.request.session['edit_mode'] = address_id
            return render(request, 'address_page.html', {'form':form, 'user_name':eludeuser.username.username,
                                                         'pop_up_address_form':'True', 'addresses':addresses})
        if 'delete-address' in request.POST:
            address_id_for_deletion = request.POST.get("delete-address")
            EludeUserAddress.objects.get(id=address_id_for_deletion).delete()
            return HttpResponseRedirect('')
        if 'make-current-address' in request.POST:
            make_current_address_id = request.POST.get("make-current-address")
            address_item = EludeUserAddress.objects.get(id=make_current_address_id)
            already_current_shipping_address = address_item.current_shipping_address
            if not already_current_shipping_address:
                try:
                    current_shipping_address_item = eludeuser.address.all().get(current_shipping_address=True)
                    current_shipping_address_item.current_shipping_address = False
                    current_shipping_address_item.save()
                except:
                    pass
                address_item.current_shipping_address = True
                address_item.save()
            try:
                    redirect_to_payment_page = self.request.session.get('redirect_to_payment_page')
            except(KeyError,TypeError, None):
                    redirect_to_payment_page = None
            if redirect_to_payment_page:
                    del self.request.session['redirect_to_payment_page']
                    return HttpResponseRedirect(reverse('cart_page', kwargs={'user_name':eludeuser.username.username}))
            return HttpResponseRedirect('')
        if form.is_valid():
            try:
                edit_mode_id_check = self.request.session.get('edit_mode', False)
                address_edited_id = edit_mode_id_check
                edit_address = EludeUserAddress.objects.get(id=address_edited_id)
            except(KeyError, TypeError, ObjectDoesNotExist):
                edit_mode_id_check = False
                edit_address = False
            if edit_mode_id_check:
                edit_address.address = form.cleaned_data.get('address')
                edit_address.city = form.cleaned_data.get('city')
                edit_address.state = form.cleaned_data.get('state')
                edit_address.zip_code = form.cleaned_data.get('zip_code')
                edit_address.save()
                del self.request.session['edit_mode']
                return HttpResponseRedirect(reverse('address_entry_page', kwargs={'user_name':eludeuser.username.username}))
            else:
                address = form.cleaned_data.get('address')
                city = form.cleaned_data.get('city')
                state = form.cleaned_data.get('state')
                zip_code = form.cleaned_data.get('zip_code')
                address = EludeUserAddress(address=address, city=city, zip_code=zip_code, state=state)
                try:
                    current_shipping_address = eludeuser.address.all().filter(current_shipping_address=True)
                except(None, KeyError, TypeError):
                    current_shipping_address = None
                if not current_shipping_address:
                    address.current_shipping_address = True
                address.save()
                eludeuser.address.add(address)
                eludeuser.save()
                try:
                    redirect_to_payment_page = self.request.session.get('redirect_to_payment_page')
                    redirect_to_stripe_connection_page = self.request.session.get('redirect_to_stripe_listing_page')
                except(KeyError,TypeError, None):
                    redirect_to_payment_page = None
                    redirect_to_stripe_connection_page = None
                if redirect_to_payment_page:
                    del self.request.session['redirect_to_payment_page']
                    return HttpResponseRedirect(reverse('cart_page', kwargs={'user_name':eludeuser.username.username}))
                message = variables.REGISTERED_NEW_ADDRESS_SUCCESS_MESSAGE
                if redirect_to_stripe_connection_page:
                    del self.request.session['redirect_to_stripe_listing_page']
                    self.request.session['new_message'] = "Sweet Book is Listed!"
                    return HttpResponseRedirect(reverse('list_book_confirmation_page', kwargs={'user_name':eludeuser.username.username}))
                return HttpResponseRedirect('')


class AccountView(LoginRequiredMixin, View):
    def get(self, request, user_name):
        if not request.user.is_authenticated():
            user_name = "guest"
        else:
            user_name = self.request.user.username
        return render(request, 'account_page.html', {'user_name': user_name})


class PaymentView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            application_fee = self.request.session.get('application_fee')
        except (None, KeyError, TypeError):
            application_fee = None
        if not request.user.is_authenticated():
            user_name = "guest"
        else:
            user_name = self.request.user.username

        form = form_templates.PaymentForm()
        return render(request, 'payment_page.html', {'user_name': user_name, 'form': form,
                                                     'application_fee':application_fee,
                                                     'pub_key':STRIPE_LIVE_PUBLISHABLE_KEY})

    def post(self, request):
        elude_user = EludeUser.objects.get(username=self.request.user)
        stripe.api_key = STRIPE_LIVE_SECRET_KEY
        try:
            token = request.POST.get("stripeToken")
        except KeyError:
            token = None
        checkout_cart = self.request.session.get('shopping_cart')
        if token:
            user_name = self.request.user.username
            try:
                customer = stripe.Customer.create(
                    source=token,
                    description=user_name
                )
                card_info = customer.sources['data'][0]
                #card_info = json.loads(card_info)
                try:
                    address = card_info['address_line1'] + "" + card_info['address_line2'] + ", " + card_info['address_city']
                    address_state = card_info['address_state']
                    address_zip_code = card_info['address_zip']
                    address_country = card_info['address_country']
                except:
                    address = "No adddress Given"
                    address_state = "No adddress Given"
                    address_zip_code = "No adddress Given"
                    address_country = "No adddress Given"
                exp_month = str(card_info['exp_month'])
                exp_year = str(card_info['exp_year'])
                last_4_of_card = card_info['last4']
                card_brand = card_info['brand']
                funding_type = card_info['funding']
                if elude_user.payment_card_info.count() > 0:
                    default_payment = False
                else:
                    default_payment = True
                payment_data = PaymentCardData(customer_id=customer.id, is_user_current_option=default_payment,
                                           address=address, address_state=address_state, address_zip_code=address_zip_code,
                                           address_country=address_country, exp_month=exp_month, exp_year=exp_year,
                                           last_4_of_card=last_4_of_card, card_brand=card_brand,
                                           funding_type=funding_type)
                payment_data.save()
                elude_user.payment_card_info.add(payment_data)
                elude_user.save()
            except stripe.error.CardError, e:
                body = e.json_body
                err = body['error']
                # use message to show user's card got declined
                messages.error(request, 'Sorry, But %s' % err['message'])
                return HttpResponseRedirect('')
            try:
                for book_id in checkout_cart:
                    book = get_object_or_404(Book, id=book_id)
                    book_price = int(book.sales_price) * 100
                    application_fee = application_fee_amount(book_price)
                    self.request.session['application_fee'] = application_fee
                    book_owner = book.book_owner
                    stripe.Charge.create(
                        amount=book_price,
                        currency='usd',
                        customer=payment_data.customer_id,
                        description="Sale of Book Charge",
                        application_fee=application_fee,
                        destination=book_owner.stripe_data.stripe_user_id
                    )
                start_range_of_pickup_time = datetime.now()
                end_range_of_pick_up_time = datetime.now() + timedelta(hours=24)
                start_range_of_pickup_time_str= start_range_of_pickup_time.strftime("%A %d. %B %Y")
                end_range_of_pick_up_time_str = end_range_of_pick_up_time.strftime("%A %d. %B %Y")
                address_full_query = elude_user.address.all().get(current_shipping_address=True)
                full_address = address_full_query.address + " "+ address_full_query.city + \
                               " "+ address_full_query.state + " "+address_full_query.zip_code
                for book_id in checkout_cart:
                    book = get_object_or_404(Book, id=book_id)
                    book_owner = book.book_owner
                    sold_book = SoldBooks(buyer=elude_user, seller=book_owner, book=book,
                                          order_number=generate_invoice_number(book_id))
                    sold_book.save()
                    book.book_is_sold = True
                    book.save()
                    del self.request.session['shopping_cart']
                    send_templated_mail(
                        template_name = 'user_purchase_confirmation_email',
                        from_email = 'Textdoar Team',
                        recipient_list = ['email@textdoar.com', elude_user.username.email],
                        context={
                            'first_name': elude_user.username.first_name,
                            'address': full_address,
                            'sub_total': convert_str_to_money(sold_book.book.sales_price),
                            'sales_tax': convert_str_to_money(get_buyers_fee()),
                            'order_total': convert_str_to_money(get_total_price_of_purchase(book.sales_price)),
                            'order_num': sold_book.order_number,
                            'book': sold_book.book.title,
                            'arrival_time': end_range_of_pick_up_time_str,
                            'book_condition': sold_book.book.book_edition,
                            },
                            bcc=[variables.CUSTOMER_SERVICE_EMAIL],
                        )
                    try:
                        pick_up_address_full_query = sold_book.seller.address.all().get(current_shipping_address=True)
                        pick_up_address = pick_up_address_full_query.address + " "+ pick_up_address_full_query.city + \
                               " "+ address_full_query.state + " "+pick_up_address_full_query.zip_code
                    except (KeyError, KeyError, None):
                        pick_up_address = "Sorry Couldn't retrieve a saved address for you"
                    send_templated_mail(
                        template_name = 'user_sold_confirmation',
                        from_email = 'Textdoar Team',
                        recipient_list = ['email@textdoar.com', sold_book.seller.username.email],
                        context={
                            'first_name': sold_book.seller.username.first_name,
                            'pickup_day_range': start_range_of_pickup_time_str,
                            'pickup_day_range_two': end_range_of_pick_up_time_str,
                            'book': sold_book.book.title,
                            'address': pick_up_address
                        },
                        bcc=[variables.CUSTOMER_SERVICE_EMAIL],
                    )
                    self.request.session['new_message'] = variables.MAKE_PAYMENT
                    del self.request.session['shopping_cart']
                return HttpResponseRedirect(reverse('success_url_page', kwargs={'user_name':user_name}))
            except stripe.error.CardError, e:
                body = e.json_body
                err  = body['error']
                # use message to show user's card got declined
                messages.error(request, 'Sorry, But %s' % err['message'])
            except stripe.error.RateLimitError, e:
                # Too many requests made to the API too quickly
                pass
                messages.error(request, 'Sorry, "Too many request made to the api too quickly".')
            except stripe.error.InvalidRequestError, e:
                # Invalid parameters were supplied to Stripe's API
                pass
                messages.error(request, 'Sorry, Invalid parameters were supplied to Stripe Systems.')
            except stripe.error.AuthenticationError, e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                pass
                messages.error(request, 'Sorry, Authentication with Stripes API failed.')
            except stripe.error.APIConnectionError, e:
                # Network communication with Stripe failed
                pass
                messages.error(request, 'Sorry, Network Communication With Stripe Failed.')
            except stripe.error.StripeError, e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                pass
                messages.error(request, 'Sorry, Display a very generic error to the user, and maybe send.')
            except Exception, e:
                # Something else happened, completely unrelated to Stripe
                pass
                try:
                    len(checkout_cart)
                except(None, TypeError, KeyError):
                    pass
                    return
                messages.error(request, 'Sorry, Something else happened, completely unrelated to Stripe.')
                return HttpResponseRedirect(reverse('cart_page', kwargs={'user_name': request.user.username}))
        return HttpResponseRedirect('')


class SavedCreditCardPaymentView(LoginRequiredMixin, View):

    def get(self, request, user_name):
        try:
            application_fee = self.request.session.get('application_fee')
        except (None, KeyError, TypeError):
            application_fee = None
        elude_user = EludeUser.objects.get(username=self.request.user)
        checkout_cart = self.request.session.get('shopping_cart')
        payment_data = elude_user.payment_card_info.all().get(is_user_current_option=True)
        last_four_digits = payment_data.last_4_of_card
        card_type = payment_data.card_brand
        return render(request, 'saved_payment_card_page.html', {'last_four_digits':last_four_digits,
                                                                'card_type':card_type, 'application_fee': application_fee})

    def post(self, request, user_name):
        if request.POST.get("payment"):
            stripe.api_key = STRIPE_LIVE_SECRET_KEY
            elude_user = EludeUser.objects.get(username=self.request.user)
            checkout_cart = self.request.session.get('shopping_cart')
            payment_data = elude_user.payment_card_info.all().get(is_user_current_option=True)
            try:
                for book_id in checkout_cart:
                    book = get_object_or_404(Book, id=book_id)
                    book_price = int(book.sales_price) * 100
                    application_fee = application_fee_amount(book_price/100)
                    self.request.session['application_fee'] = application_fee
                    book_owner = book.book_owner
                    stripe.Charge.create(
                        amount=book_price,
                        currency='usd',
                        customer=payment_data.customer_id,
                        description="Sale of Book Charge",
                        application_fee=application_fee,
                        destination=book_owner.stripe_data.stripe_user_id
                    )
                start_range_of_pickup_time = datetime.now() + timedelta(hours=6)
                end_range_of_pick_up_time = datetime.now() + timedelta(hours=36)
                start_range_of_pickup_time_str = start_range_of_pickup_time.strftime("%A %d. %B %Y")
                end_range_of_pick_up_time_str = end_range_of_pick_up_time.strftime("%A %d. %B %Y")
                address_full_query = elude_user.address.all().get(current_shipping_address=True)
                full_address = address_full_query.address + " "+ address_full_query.city + \
                               " "+ address_full_query.state + " "+address_full_query.zip_code
                for book_id in checkout_cart:
                    book = get_object_or_404(Book, id=book_id)
                    book_owner = book.book_owner
                    sold_book = SoldBooks(buyer=elude_user, seller=book_owner, book=book,
                                          order_number=generate_invoice_number(book.id))
                    sold_book.save()
                    book.book_is_sold = True
                    book.save()
                    send_templated_mail(
                    template_name = 'user_purchase_confirmation_email',
                    from_email = 'Textdoar Team',
                    recipient_list = ['email@textdoar.com', elude_user.username.email],
                    context={
                        'first_name': elude_user.username.first_name,
                        'address': full_address,
                        'sub_total': convert_str_to_money(sold_book.book.sales_price),
                        'sales_tax': convert_str_to_money(get_buyers_fee()),
                        'order_total': convert_str_to_money(get_total_price_of_purchase(book.sales_price)),
                        'order_num': sold_book.order_number,
                        'book': sold_book.book.title,
                        'arrival_time': end_range_of_pick_up_time_str,
                        'book_condition': sold_book.book.book_edition,
                        },
                        bcc=[variables.CUSTOMER_SERVICE_EMAIL],
                    )
                    try:
                        pick_up_address_full_query = sold_book.seller.address.all().get(current_shipping_address=True)
                        pick_up_address = pick_up_address_full_query.address + " "+ pick_up_address_full_query.city + \
                               " "+ address_full_query.state + " "+pick_up_address_full_query.zip_code
                    except (KeyError, KeyError, None):
                        pick_up_address = "Sorry Couldn't retrieve a saved address for you"
                    send_templated_mail(
                    template_name = 'user_sold_confirmation',
                    from_email = 'Textdoar Team',
                    recipient_list = ['email@textdoar.com', sold_book.seller.username.email],
                    context={
                        'first_name': sold_book.seller.username.first_name,
                        'pickup_day_range': start_range_of_pickup_time_str,
                         'pickup_day_range_two': end_range_of_pick_up_time_str,
                        'book': sold_book.book.title,
                        'address': pick_up_address
                        },
                        bcc=[variables.CUSTOMER_SERVICE_EMAIL],
                    )
                    self.request.session['new_message'] = variables.MAKE_PAYMENT
                    try:
                        del self.request.session['shopping_cart']
                    except (KeyError, TypeError):
                        pass
                return HttpResponseRedirect(reverse('success_url_page', kwargs={'user_name': request.user.username}))
            except stripe.error.CardError, e:
                body = e.json_body
                err  = body['error']
                # use message to show user's card got declined
                messages.error(request, 'Sorry, But %s' % err['message'])
            except stripe.error.RateLimitError, e:
                # Too many requests made to the API too quickly
                pass
                messages.error(request, 'Sorry, we encountered while processing your card.')
            except stripe.error.InvalidRequestError, e:
                # Invalid parameters were supplied to Stripe's API
                pass
                messages.error(request, 'Sorry, we encountered while processing your card.')
            except stripe.error.AuthenticationError, e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                pass
                messages.error(request, 'Sorry, we encountered while processing your card.')
            except stripe.error.APIConnectionError, e:
                # Network communication with Stripe failed
                pass
                messages.error(request, 'Sorry, we encountered while processing your card.')
            except stripe.error.StripeError, e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                pass
                messages.error(request, 'Sorry, we encountered while processing your card.')
            except Exception, e:
                # Something else happened, completely unrelated to Stripe
                pass
                try:
                    len(checkout_cart)
                except(None, TypeError, KeyError):
                    pass
                    return
                messages.error(request, 'Sorry, Something else happened, completely unrelated to Stripe.')
                return HttpResponseRedirect(reverse('cart_page', kwargs={'user_name': request.user.username}))
            return HttpResponseRedirect('')


# allows us access to user's stripe account
class StripeConnectionConfirmationView(LoginRequiredMixin, View):

    def get(self, request):
        try:
            session = self.request.session.get('stripe_data')
        except (TypeError, KeyError):
            session = None
        try:
            code = request.GET.get('code', '')
            scope = request.GET.get('scope', '')
        except:
            code = None
            scope = None
        return render(request, 'stripe_connection_confirmation_page.html', {'code': code,
                                                                  'scope': scope, 'session':session
                                                                  })

    def post(self, request):
        elude_user = EludeUser.objects.get(username=self.request.user)
        if request.POST.get("complete-connection") or request.POST.get("complete-connection-non-modal"):
            code = request.POST.get("code")
            if code:
                response_dict = {'code': code, 'client_secret':"sk_test_0nUBiJyARoPOsmheLyUv4Glq",
                            'grant_type': "authorization_code"}
                session = stripe_token.get_raw_access_token(data=response_dict)
                self.request.session['stripe_data'] = session.json()
                value_dic = session.json()
                try:
                    stripe_data = StripeData(token_type=value_dic['token_type'],
                                         stripe_publishable_key=value_dic['stripe_publishable_key'],
                                         scope=value_dic['scope'], stripe_user_id=value_dic['stripe_user_id'],
                                         refresh_token=value_dic['refresh_token'],
                                         access_token=value_dic['access_token'])
                    elude_user.stripe_account_activated = True
                    stripe_data.save()
                    elude_user.stripe_data = stripe_data
                    elude_user.save(force_update=True)
                    self.request.session['message_for_success'] = variables.LIST_BOOK_MESSAGE
                    if elude_user.address.count() is 0:
                        self.request.session['redirect_to_success_page'] = True
                        return HttpResponseRedirect(reverse('address_entry_page',
                                                            kwargs={'user_name':elude_user.username.username}))
                    return HttpResponseRedirect(reverse('success_url_page',
                                                        kwargs={"user_name":elude_user.username.username}))
                except (TypeError, KeyError, ValueError):
                    pass
            return HttpResponseRedirect(reverse('error_page_for_stripe', kwargs={"user_name":elude_user.username.username}))
        return HttpResponseRedirect('')


class ListBookConfirmationView(LoginRequiredMixin, View):

    def get(self, request, user_name):
        elude_user = EludeUser.objects.get(username=self.request.user)
        try:
            address = elude_user.address.all().get(current_shipping_address=True)
        except (KeyError, None, TypeError):
            address = None
        if elude_user.address.count() is 0 or (address is None):
            self.request.session['redirect_to_stripe_listing_page'] = "True"
            return HttpResponseRedirect(reverse('address_entry_page',
                                                kwargs={'user_name': elude_user.username.username}))
        stripe_user_email = elude_user.username.email
        stripe_user_url = 'https://www.textdoar.com/'+elude_user.username.username+'/'
        stripe_user_country = 'US'
        stripe_user_phone_number = elude_user.phone_number
        stripe_user_business_name = "textdoar"
        stripe_user_first_name = elude_user.username.first_name
        stripe_user_last_name = elude_user.username.last_name
        stripe_user_street_address = address.address
        stripe_user_city = address.city
        stripe_user_state = address.state
        stripe_user_zip_code = address.zip_code
        stripe_user_product = "true"
        stripe_user_shipping_days = 2
        stripe_user_product_category = "education"
        stripe_user_product_description = "the sale of used textbooks to student"
        stripe_user_average_payment = 37
        stripe_user_past_year_volume = 160
        stripe_user_currency = 'usd'
        stripe_user_business_type = "sole_prop"
        return render(request, 'list_book_confirmation_page.html', {'stripe_user_email':stripe_user_email,
                                                                  'stripe_user_url':stripe_user_url, 'stripe_user_country':stripe_user_country, 'stripe_user_phone_numbe':stripe_user_phone_number, 'stripe_user_business_name':
                                                                  stripe_user_business_name, 'stripe_user_first_name':stripe_user_first_name,
                                                                  'stripe_user_last_name':stripe_user_last_name,
                                                                  'stripe_user_street_address':stripe_user_street_address,
                                                                   'stripe_user_city':stripe_user_city, 'stripe_user_state':
                                                                   stripe_user_state, 'stripe_user_zip_code':stripe_user_zip_code,
                                                                  'stripe_user_product':stripe_user_product,
                                                                  'stripe_user_shipping_days':stripe_user_shipping_days,
                                                                  'stripe_user_product_category':stripe_user_product_category,
                                                                  'stripe_user_product_description':stripe_user_product_description,
                                                                  'stripe_user_average_payment':stripe_user_average_payment,
                                                                  'stripe_user_past_year_volume':stripe_user_past_year_volume,
                                                                  'stripe_user_currency':stripe_user_currency,
                                                                'stripe_user_business_type':stripe_user_business_type})


class ChangePasswordView(LoginRequiredMixin, View):

    def get(self, request, user_name):
        user = User.objects.get(username=self.request.user.username)
        form = form_templates.PasswordChangeForm()
        return render(request, 'password_change_page.html', {'user_name':user.username, 'form':form})

    def post(self, request, user_name):
        form = form_templates.PasswordChangeForm(request.POST)
        user = User.objects.get(username=self.request.user.username)
        if form.is_valid():
            new_password = form.cleaned_data.get("password")
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Sweet! Password Has Been Changed!')
            update_session_auth_hash(request, user)
            return HttpResponseRedirect('')
        else:
            return render(request, 'password_change_page.html', {'form': form})


class OrderHistoryView(LoginRequiredMixin, View):

    def get(self, request, user_name):
        users_purchased_books_list = []
        users_sold_books_list = []
        elude_user = EludeUser.objects.get(username=self.request.user)
        try:
            users_purchased_books = SoldBooks.objects.filter(buyer=elude_user)
            users_sold_books = SoldBooks.objects.filter(seller=elude_user)
        except None:
            users_purchased_books = None
            users_sold_books = None
        if users_purchased_books:
            for book in users_purchased_books:
                    book_image = BookImage.objects.filter(book=book.book).values()
                    users_purchased_books_list.append((book, book_image))
        if users_sold_books:
            for book in users_sold_books:
                    book_image = BookImage.objects.filter(book=book.book).values()
                    users_sold_books_list.append((book, book_image))
        return render(request, 'order_history.html', {'user_name':user_name,
                                                      'user_purchased_books':users_purchased_books_list,
                                                      'user_sold_books': users_sold_books_list})


class PaymentCardDetailView(LoginRequiredMixin, View):

    def get(self, request, user_name):
        elude_user = EludeUser.objects.get(username=self.request.user)
        saved_card_details = elude_user.payment_card_info.all()
        return render(request, 'payment_card_details_page.html', {'user_name':user_name,
                                                                  'saved_card_info': saved_card_details,
                                                                  })

    def post(self, request, user_name):
        elude_user = EludeUser.objects.get(username=self.request.user)
        if 'delete-card-id' in request.POST:
            card_id_for_deletion = request.POST.get("delete-card-id")
            PaymentCardData.objects.get(id=card_id_for_deletion).delete()
            return HttpResponseRedirect('')
        if 'make-default-card-id' in request.POST:
            make_card_default_id = request.POST.get("make-default-card-id")
            card_item = PaymentCardData.objects.get(id=make_card_default_id)
            already_default_card_option = card_item.is_user_current_option
            if not already_default_card_option:
                try:
                    current_default_card_option = elude_user.payment_card_info.all().get(is_user_current_option=True)
                    current_default_card_option.is_user_current_option = False
                    current_default_card_option.save()
                except:
                    pass
                card_item.current_shipping_address = True
                card_item.save()
            return HttpResponseRedirect('')


class ErrorPageViewForStripe(LoginRequiredMixin, View):

    def get(self, request, user_name):
        elude_user = EludeUser.objects.get(username=self.request.user)
        return render(request, 'error_page_for_stripe.html', {'user_name':elude_user.username.username})


class AboutUSView(View):

    def get(self, request):
        if request.user.is_authenticated():
            user_name = request.user.username
        else:
            user_name = "guest"
        return render(request, 'about_us.html', {'user_name':user_name})


class ContactUSView(View):

    def get(self, request):
        form = form_templates.StudentFeedBacksForm()
        if request.user.is_authenticated():
            user_name = request.user.username
        else:
            user_name = "guest"
        return render(request, 'contact_us.html', {'form':form, 'user_name':user_name})

    def post(self, request):
        form = form_templates.StudentFeedBacksForm(request.POST)
        if form.is_valid():
            topic = form.cleaned_data.get('topic')
            email = form.cleaned_data.get('user_email')
            feed_back = form.cleaned_data.get('feed_back')
            student_feed_back = StudentFeedBacks(email=email, feed_back=feed_back, topic=topic)
            student_feed_back.save()
            if email:
                sending_list = ['email@textdoar.com', email]
            else:
                sending_list = ['emai@textdoar.com']
            send_templated_mail(
                template_name = 'feed_back_receive_email',
                from_email = 'Textdoar Team',
                recipient_list = sending_list, #testing purposes
                context={
                    'email': email,
                    'topic': topic,
                    'feed_back': feed_back,
                        },
                        bcc=[variables.CUSTOMER_SERVICE_EMAIL],
                )
            messages.success(request, 'Sweet, thanks for your feedback')
        else:
            return render(request, 'contact_us.html', {'form': form})
        return HttpResponseRedirect('')


class TermAndConditionView(View):

    def get(self, request):
        if request.user.is_authenticated():
            user_name = request.user.username
        else:
            user_name = "guest"
        return render(request, 'term_and_condition_page.html', {'user_name':user_name})









