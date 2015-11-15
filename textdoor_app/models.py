from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify



class EludeUser(models.Model):
    username = models.OneToOneField(User, default='')
    college_attending = models.CharField(max_length=254)
    new_user = models.BooleanField(default=True)

    def __str__(self):
        return self.username.username


class Book(models.Model):
    title = models.CharField(max_length=500)
    isbn_number = models.CharField(max_length=500)
    long_term_rent = models.BooleanField(default=False)
    short_term_rent = models.BooleanField(default=False)
    for_buy = models.BooleanField(default=False)
    book_condition = models.CharField(max_length=25)
    for_trade = models.BooleanField(default=False)
    need_investment = models.BooleanField(default=False)
    author = models.CharField(max_length=500)
    price = models.FloatField(default=0.00)
    publish_date = models.DateTimeField(db_index=True, blank=True, default=datetime.now)
    book_owner = models.ForeignKey(EludeUser, default='')
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single_book_description', args=(self.pk, self.id, self.slug ))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)


class Watchlist(models.Model):
    book = models.ForeignKey(Book, default='No book on watch list')
    user = models.ForeignKey(EludeUser)

    def __str__(self):
        return self.book.title

class OrderHistory(models.Model):
    book = models.ForeignKey(Book, default='No order history')
    user = models.ForeignKey(EludeUser)

    def __str__(self):
        return self.user.username


class BookImage(models.Model):
    image_name = models.CharField(max_length=100)
    book_image = models.ImageField(upload_to='image/%Y/%m/%d', verbose_name="book image")
    book = models.ForeignKey(Book, default='')

    def __str__(self):
        return self.image_name

class MerchantGroup(models.Model):
    user = models.ForeignKey(EludeUser)


class StudentGroup(models.Model):
    user = models.ForeignKey(EludeUser)


class NonStudentGroup(models.Model):
    user = models.ForeignKey(EludeUser)


class RepGroup(models.Model):
    user = models.ForeignKey(EludeUser)


class BookRentedOut(models.Model):
    user = models.ForeignKey(EludeUser)
    book = models.ForeignKey(Book)
    time_received = models.DateTimeField(verbose_name="Time book was received")
    additional_information = models.TextField(verbose_name="Additional Information about book rental i.e length of rent")
    time_book_was_rented_out = models.DateTimeField(verbose_name="Time book was rented out")
    has_book_been_returned = models.BooleanField(default=False, verbose_name="Has book been Returned")
    type_of_rent = models.CharField(default=None, verbose_name="Length of Book's Rent", max_length=250)
    price = models.CharField(default=None, max_length=250)

class BookYouAreRenting(models.Model):
    user = models.ForeignKey(EludeUser)
    book = models.ForeignKey(Book)
    time_received = models.DateTimeField(verbose_name="Time renting began")
    additional_information = models.TextField(verbose_name="Additional Information about book rental i.e length of rent")
    time_book_was_rented_out = models.DateTimeField(verbose_name="Time renting ended or should end")
    has_book_been_returned = models.BooleanField(default=False, verbose_name="Has book been Returned to owner?")
    type_of_rent = models.CharField(default='None', verbose_name="Length of Book's Rent", max_length=250)
    price = models.CharField(default=None, max_length=250)

class BookTradingOut(models.Model):
    user = models.ForeignKey(EludeUser)
    book = models.ForeignKey(Book, related_name='your_book')
    time_received = models.DateTimeField(verbose_name="Time book was received", default=None)
    additional_information = models.TextField(verbose_name="Additional Information about book trade i.e length of trade")
    length_of_trade = models.CharField(verbose_name="Length of trade", default='None', max_length=250)
    has_book_been_returned = models.BooleanField(default=False, verbose_name="Has book been Returned")
    item_traded_for_if_not_book = models.CharField(default=None, verbose_name="Item traded for, if not book", max_length=250)
    book_gotten_in_trade = models.ForeignKey(Book, related_name='book_gotten_in_trade')
    time_book_was_traded = models.DateTimeField(verbose_name="Time book was traded out", default=None)
    price = models.CharField(default=None, max_length=250)


class BookYouSold(models.Model):
    user = models.ForeignKey(EludeUser)
    book = models.ForeignKey(Book)
    additional_information = models.TextField(verbose_name="Additional Information about book sold")
    time_book_was_sold = models.DateTimeField(verbose_name="Time book was sold")
    price = models.CharField(default=None, max_length=250)


class BookYouBought(models.Model):
    user = models.ForeignKey(EludeUser)
    book = models.ForeignKey(Book)
    additional_information = models.TextField(verbose_name="Additional Information about book rental i.e length of rent")
    time_book_was_bought = models.DateTimeField(verbose_name="Time book was bought")
    price = models.CharField(default=None, max_length=250)

class NewTransactionProcess(models.Model):
    user = models.ForeignKey(EludeUser, default="guest")
    book = models.ManyToManyField(Book)
    slug = models.SlugField()
    at_least_one_book_sold = models.BooleanField(default=False, verbose_name="Check if user bought at least a textbook")




