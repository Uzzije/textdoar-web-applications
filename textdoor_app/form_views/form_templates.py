__author__ = 'Administrator'
from django import forms
from textdoor_app.models import User, LaunchPageEmail
from ..choices import SCHOOL_LIST, BOOK_CONDITION, FEED_BACK_TOPICS, EXPIRATION_YEAR_CHOICES, EXPIRATION_MONTH_CHOICES
from localflavor.us.forms import USStateSelect, USZipCodeField, USStateField
from datetime import date
from calendar import monthrange
from ..helper_functions import validate_activation_code, card_type

SCHOOL_LIST_IN_ORDER = sorted(SCHOOL_LIST)


class UserSignUpForm(forms.Form):

    user_name = forms.CharField(label='User Name', max_length=100, required=False)
    first_name = forms.CharField(label='First Name', max_length=100, required=True)
    last_name = forms.CharField(label='Last Name', max_length=100, required=True)
    email = forms.EmailField(label='Email (ending in edu)', max_length=100, required=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(),
                               required=True)
    verify_password = forms.CharField(label='Verify Password', widget=forms.PasswordInput(), required=True)
    user_college = forms.ChoiceField(label="Your University", choices=SCHOOL_LIST_IN_ORDER, widget=forms.Select(),
                                     required=True)

    def clean(self):
            cleaned_data = super(UserSignUpForm, self).clean()
            user_password = self.cleaned_data.get('password')
            user_verify_password = self.cleaned_data.get('verify_password')

            if user_password and user_verify_password:
                if user_password != user_verify_password:
                    msg = "Passwords does not match"
                    self.add_error('password', msg)
            return cleaned_data

    def clean_user_name(self):
        cleaned_data = super(UserSignUpForm, self).clean()
        user_name = self.cleaned_data['user_name']
        try:
            User.objects.get(username=user_name)
            msg = "Username already in use"
            self.add_error('user_name', msg)
        except User.DoesNotExist:
            if len(user_name) < 3:
                msg = "Username already in use"
                self.add_error('user_name', msg)
            elif user_name is not "guest":
                return user_name

    def clean_email(self):
        cleaned_data = super(UserSignUpForm, self).clean()
        email = self.cleaned_data['email']
        email_suffix = "edu"
        try:
            email_value = User.objects.get(email=email)
            msg = "hmm, this email is already in use"
            self.add_error('email', msg)
        except User.DoesNotExist:
            if email.endswith(email_suffix):
                return email
            else:
                msg = "sorry, email address must end in 'edu' "
                self.add_error('email', msg)


class ActivateAccountForm(forms.Form):
    code = forms.CharField(label='Enter Code', required=False)

    def clean_code(self):
        cleaned_data = super(ActivateAccountForm, self).clean()
        code = self.cleaned_data.get('code')
        if validate_activation_code(code):
            return code
        msg = 'sorry code is not valid'
        self.add_error('code', msg)


class PasswordChangeForm(forms.Form):
    password = forms.CharField(label='Set New Password', widget=forms.PasswordInput(),
                               required=True)
    verify_password = forms.CharField(label='Verify New Password', widget=forms.PasswordInput(), required=True)

    def clean(self):
            cleaned_data = super(PasswordChangeForm, self).clean()
            user_password = self.cleaned_data.get('password')
            user_verify_password = self.cleaned_data.get('verify_password')

            if user_password and user_verify_password:
                if user_password != user_verify_password:
                    msg = "Passwords does not match"
                    self.add_error('password', msg)
            return cleaned_data


class LogInForm(forms.Form):
    my_default_errors = {
        'invalid': 'Make sure username and password are correct'
    }
    name = forms.CharField(label='User Name', max_length=100, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), error_messages=my_default_errors)

    def clean_name(self):
        cleaned_data = super(LogInForm, self).clean()
        name = self.cleaned_data['name']
        try:
            user = User.objects.get(username=name)
        except User.DoesNotExist:
            user = None
        if user is None:
            msg = " Oops Username does not exist"
            self.add_error('name', msg)
        else:
            return user


class AddressBookForm(forms.Form):
    address = forms.CharField(label='Address', max_length=None, required=True, widget=forms.TextInput(attrs={'name':'address'}))
    city = forms.CharField(label='City', max_length=None, required=True,
                           widget=forms.TextInput(attrs={'name':'city'}))
    zip_code = USZipCodeField(required=True,
                              widget=forms.TextInput(attrs={'name':'zip_code'}))
    state = USStateField(required=True, widget=USStateSelect(attrs={'name':'state'}), label="State")


class RegisterBookForm(forms.Form):
    book_name = forms.CharField(label='Name of Book', max_length=None, required=True)
    author = forms.CharField(label='Author', max_length=None, required=True)
    isbn = forms.CharField(max_length=500, label='ISBN Number')
    images = forms.ImageField(label='Upload Your Own Image(Optional)', required=False)
    book_condition = forms.ChoiceField(label='Book Condition', choices=BOOK_CONDITION, widget=forms.Select(),
                                       required=True)
    book_edition = forms.CharField(max_length=100, label="Book Edition (leave blank if no volume or edition has been issued to book)",
                                   required=False, widget=forms.TextInput(attrs={'placeholder': 'i.e Volume 1 or Edition 1'}))
    book_price = forms.CharField(max_length=100, label="Selling Price($)", required=True)
    book_description = forms.CharField(max_length=5000, label="Is there anything else you would like the buyer "
                                                             "to know about this book (optional)",
                                       widget=forms.Textarea(attrs={'placeholder': 'i.e Has a big water mark stain on page 7'}),
    required=False)

    def clean_book_price(self):
        cleaned_data = super(RegisterBookForm, self).clean()
        price = self.cleaned_data['book_price']
        try:
            int(price)
            return price
        except:
            msg = "Input must be a number"
            self.add_error('book_price', msg)


class CreditCardField(forms.IntegerField):
  def get_cc_type(self, number):
    """
    Gets credit card type given number. Based on values from Wikipedia page
    "Credit card number".
    <a href="http://en.wikipedia.org/w/index.php?title=Credit_card_number
">http://en.wikipedia.org/w/index.php?title=Credit_card_number
</a>    """
    number = str(number)
    #group checking by ascending length of number
    if len(number) == 13:
      if number[0] == "4":
        return "Visa"
    elif len(number) == 14:
      if number[:2] == "36":
        return "MasterCard"
    elif len(number) == 15:
      if number[:2] in ("34", "37"):
        return "American Express"
    elif len(number) == 16:
      if number[:4] == "6011":
        return "Discover"
      if number[:2] in ("51", "52", "53", "54", "55"):
        return "MasterCard"
      if number[0] == "4":
        return "Visa"
    return "Unknown"

  def clean(self, value):
    """Check if given CC number is valid and one of the
    card types we accept"""
    try:
        check_value = int(value)
    except:
        check_value = None
    if value and (len(value) < 13 or len(value) > 16 or check_value is None):
        msg = "Please enter in a valid "+\
          "credit card number."
        self.add_error('password', msg)
    elif self.get_cc_type(value) not in ("Visa", "MasterCard",
        "American Express", "Discover"):
        msg = "Please enter in a Visa, "+\
          "Master Card, Discover, or American Express credit card number."
        self.add_error('password', msg)
    else:
        return super(CreditCardField, self).clean(value)


class PaymentForm(forms.Form):
  number = CreditCardField(required=True, label = "Card Number",
                           widget=forms.TextInput(attrs={'data-stripe':'number', 'class':'card-number'}))
  name = forms.CharField(required=True, label="Card Holder Full Name", max_length=30,
                               widget=forms.TextInput(attrs={'data-stripe':'name'}))
  expire_month = forms.ChoiceField(required=True, choices=EXPIRATION_MONTH_CHOICES,
                                   widget=forms.Select(attrs={'data-stripe':'exp_month','class':'card-expiry-month'}))
  expire_year = forms.ChoiceField(required=True, choices=EXPIRATION_YEAR_CHOICES,
                                  widget=forms.Select(attrs={'data-stripe':'exp_year', 'class': 'card-expiry-year'}))
  cvv_number = forms.IntegerField(required = True, label = "CVV Number",
      max_value = 9999, widget = forms.TextInput(attrs={'size': '4', 'data-stripe': 'cvc', 'class':'card-number'}))

  def __init__(self, *args, **kwargs):
    self.payment_data = kwargs.pop('payment_data', None)
    super(PaymentForm, self).__init__(*args, **kwargs)

  def clean(self):
    cleaned_data = super(PaymentForm, self).clean()
    expire_month = cleaned_data.get('expire_month')
    expire_year = cleaned_data.get('expire_year')

    if expire_year in forms.fields.EMPTY_VALUES:
      #raise forms.ValidationError("You must select a valid Expiration year.")
      self._errors["expire_year"] = self.error_class(["You must select a valid Expiration year."])
      del cleaned_data["expire_year"]
    if expire_month in forms.fields.EMPTY_VALUES:
      #raise forms.ValidationError("You must select a valid Expiration month.")
      self._errors["expire_month"] = self.error_class(["You must select a valid Expiration month."])
      del cleaned_data["expire_month"]
    year = int(expire_year)
    month = int(expire_month)
    # find last day of the month
    day = monthrange(year, month)[1]
    expire = date(year, month, day)

    if date.today() > expire:
      #raise forms.ValidationError("The expiration date you entered is in the past.")
      self._errors["expire_year"] = self.error_class(["The expiration date you entered is in the past."])

    return cleaned_data

  def clean_number(self):
        cleaned_data = super(PaymentForm, self).clean()
        number = self.cleaned_data['number']
        value = card_type(number)
        try:
            check_value = int(value)
        except:
            check_value = None
        if value and (len(value) < 13 or len(value) > 16 or check_value is None):
            msg = "Please enter in a valid "+\
            "credit card number."
            self.add_error('number', msg)
        elif self.get_cc_type(value) not in ("Visa", "MasterCard",
            "American Express", "Discover"):
            msg = "Please enter in a Visa, "+\
            "Master Card, Discover, or American Express credit card number."
            self.add_error('number', msg)
        else:
            return super(PaymentForm, self).clean(value)


class StudentFeedBacksForm(forms.Form):

    topic = forms.ChoiceField(label='Choose Topic', choices=FEED_BACK_TOPICS, widget=forms.Select(),
                                       required=True)
    feed_back = forms.CharField(max_length=5000, label="Your FeedBack or Question",
                                       widget=forms.Textarea(attrs={'placeholder': 'i.e When was textdoar created?'}),
    required=True)
    user_email = forms.CharField(max_length=1000, label="Enter Email(optional)", required=False)

    def clean_feed_back(self):
        cleaned_data = super(StudentFeedBacksForm, self).clean()
        feed_back = self.cleaned_data['feed_back']
        if len(feed_back) is 0:
            msg = " Oops You Forgot To Write Something"
            self.add_error('name', msg)
        elif len(feed_back) > 2000:
            msg = "Wow, that's alot of words, have mercy on our poor database"
            self.add_error('name', msg)
        else:
            return feed_back


class BooksStudentNeedForm(forms.Form):
    isbn_number = forms.CharField(max_length=5000, label="Enter ISBN Number",
                                       widget=forms.TextInput(attrs={'placeholder': 'Enter ISBN number here'}),required=True)
    email = forms.EmailField(max_length=5000, label="Your Email To Notify You", required=False)
    name_of_book = forms.CharField(max_length=5000, label="Name of Book (optional)", required=False)


class LaunchPageForm(forms.Form):
    user_email = forms.EmailField(max_length=50, label="Enter Your Email Here", required=True)

class UnsubcribeForm(forms.Form):
    user_email = forms.EmailField(max_length=50, label="Verify Your Email Here", required=True)

    def clean(self):
        cleaned_data = super(UnsubcribeForm, self).clean()
        email = self.cleaned_data['user_email']
        try:
            User.objects.get(email=email)
            return email
        except User.DoesNotExist:
                msg = "sorry, email deosn't exist in our database"
                self.add_error('user_email', msg)

