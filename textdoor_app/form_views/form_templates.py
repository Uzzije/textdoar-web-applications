__author__ = 'Administrator'
from django import forms
from textdoor_app.models import User
from ..choices import SCHOOL_LIST, BOOK_CONDITION
from localflavor.us.forms import USStateSelect, USZipCodeField, USStateField
from datetime import date
from calendar import monthrange

SCHOOL_LIST_IN_ORDER = sorted(SCHOOL_LIST)


class UserSignUpForm(forms.Form):

    user_name = forms.CharField(label='User Name', max_length=100, required=False)
    first_name = forms.CharField(label='First Name', max_length=100, required=True)
    last_name = forms.CharField(label='Last Name', max_length=100, required=True)
    email = forms.EmailField(label='Email', max_length=100, required=False)
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
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            if user_name is not "guest":
                return user_name
        msg = "Username already in use"
        self.add_error('user_name', msg)

    def clean_email(self):
        cleaned_data = super(UserSignUpForm, self).clean()
        email = self.cleaned_data['email']
        try:
            email = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        msg = "Email already registered"
        self.add_error('email', msg)


class LogInForm(forms.Form):
    my_default_errors = {
        'invalid': 'Make sure username and password are correct'
    }
    name = forms.CharField(label='User Name', max_length=100)
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
    address = forms.CharField(label='Address', max_length=None, required=True, widget=forms.TextInput)
    city = forms.CharField(label='City', max_length=None, required=True)
    zip_code = USZipCodeField(required=True)
    state = USStateField(required=True, widget=USStateSelect, label="State")


class RegisterBookForm(forms.Form):
    book_name = forms.CharField(label='Name of Book', max_length=None, required=True)
    author = forms.CharField(label='Author', max_length=None, required=True)
    isbn = forms.CharField(max_length=500, label='ISBN Number')
    images = forms.ImageField(label='Upload Your Own Image(Optional)', required=False)
    book_condition = forms.ChoiceField(label='Book Condition', choices=BOOK_CONDITION, widget=forms.Select(),
                                       required=True)
    book_edition = forms.CharField(max_length=100, label="Book Edition (leave blank if no volume or edition has been issued to book)",
                                   required=False)
    book_price = forms.CharField(max_length=100, label="Selling Price($)", required=True)
    book_description = forms.CharField(max_length=5000, label="Is there anything else you would like the buyer "
                                                             "to know about this book (Optional)", widget=forms.Textarea,
    required=False)


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
    if value and (len(value) < 13 or len(value) > 16):
      raise forms.ValidationError("Please enter in a valid "+\
          "credit card number.")
    elif self.get_cc_type(value) not in ("Visa", "MasterCard",
        "American Express", "Discover"):

      raise forms.ValidationError("Please enter in a Visa, "+\
          "Master Card, Discover, or American Express credit card number.")

    return super(CreditCardField, self).clean(value)


class PaymentForm(forms.Form):
  number = CreditCardField(required = True, label = "Card Number")
  first_name = forms.CharField(required=True, label="Card Holder First Name", max_length=30)
  last_name = forms.CharField(required=True, label="Card Holder Last Name", max_length=30)
  expire_month = forms.ChoiceField(required=True, choices=[(x, x) for x in xrange(1, 13)])
  expire_year = forms.ChoiceField(required=True, choices=[(x, x) for x in xrange(date.today().year, date.today().year + 15)])
  cvv_number = forms.IntegerField(required = True, label = "CVV Number",
      max_value = 9999, widget = forms.TextInput(attrs={'size': '4'}))

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