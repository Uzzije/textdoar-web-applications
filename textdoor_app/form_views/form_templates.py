from django import forms
from textdoor_app.models import User
from ..choices import SCHOOL_LIST, BOOK_CONDITION
__author__ = 'Administrator'

'Create for user to sign in/get registered do that today http://www.djangobook.com/en/2.0/chapter14.html'
'Create user profile page, with single button to list page'
'Create a list new item form'
'Create your books page'
'http://haystacksearch.org/ search engine'


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
        'required': 'Make sure username and password are correct',
        'invalid': 'Make sure username and password are correct'
    }
    name = forms.CharField(label='User Name', max_length=100, error_messages=my_default_errors)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), error_messages=my_default_errors)


class RegisterBookForm(forms.Form):
    book_name = forms.CharField(label='Name of Book', max_length=None, required=True)
    author = forms.CharField(label='Author', max_length=None, required=True)
    isbn = forms.CharField(max_length=500, label='ISBN Number')
    images = forms.ImageField(label='Book Images', required=False)
    book_condition = forms.ChoiceField(label='Book Condition', choices=BOOK_CONDITION, widget=forms.Select(),
                                       required=True)
    price = forms.FloatField(label='Suggest Price of Book', required=True)




