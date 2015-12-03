from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from image_cropping import ImageRatioField


class EludeUserAddress(models.Model):
    address = models.CharField(default=None, max_length=600)
    city = models.CharField(default=None, max_length=600)
    state = models.CharField(default=None, max_length=600)
    zip_code = models.CharField(default=None, max_length=600)


class EludeUser(models.Model):
    username = models.OneToOneField(User, default='')
    college_attending = models.CharField(max_length=254)
    new_user = models.BooleanField(default=True)
    address = models.ManyToManyField(EludeUserAddress)

    def __str__(self):
        return self.username.username


class Book(models.Model):
    title = models.CharField(db_index=True, max_length=500)
    isbn_number = models.CharField(db_index=True, max_length=500)
    long_term_rent = models.BooleanField(default=False)
    short_term_rent = models.BooleanField(default=False)
    for_buy = models.BooleanField(default=False)
    book_condition = models.CharField(max_length=25)
    need_investment = models.BooleanField(default=False)
    author = models.CharField(max_length=500)
    sales_price = models.CharField(default="0.00", max_length=500)
    rent_price = models.CharField(default="0.00", max_length=500)
    short_term_rent_price = models.CharField(default="0.00", max_length=500)
    eight_weeks_rent_price = models.CharField(default="0.00", max_length=500)
    publish_date = models.DateTimeField(db_index=True, blank=True, default=datetime.now)
    book_owner = models.ForeignKey(EludeUser, default='')
    slug = models.SlugField(max_length=100)

    #come back to this search later
    #objects = SearchManager(('title', 'isbn_number', 'author'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single_book_description', args=(self.id, self.slug))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify("%s%s" % (self.title, str(self.id)))
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
    cropping = ImageRatioField('book_image', '430x360')

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


class BookAcquiredByRent(models.Model):
    user = models.ForeignKey(EludeUser)
    book = models.ForeignKey(Book)
    rented_date = models.DateTimeField()
    additional_information = models.TextField()
    return_date = models.DateTimeField()
    has_book_been_returned = models.BooleanField(default=False)
    type_of_rent = models.CharField(default=None, max_length=250)


class BookListedAsRent(models.Model):
    user = models.ForeignKey(EludeUser)
    book = models.ForeignKey(Book)
    time_received = models.DateTimeField(auto_now_add=True)
    additional_information = models.TextField()
    return_date = models.DateTimeField()
    type_of_rent = models.CharField(default='None',
                                    max_length=250)


class BooksYourAreRenting(models.Model):
    user = models.ForeignKey(EludeUser)
    book = models.ForeignKey(BookListedAsRent, related_name='your_book')
    has_book_been_returned = models.BooleanField(default=False)


class ListedBookForSale(models.Model):
    user = models.ForeignKey(EludeUser)
    book = models.ForeignKey(Book)
    additional_information = models.TextField(default="No additional information")


class SoldBooks(models.Model):
    user = models.ForeignKey(EludeUser)
    book = models.ForeignKey(ListedBookForSale)
    time_book_was_sold = models.DateTimeField()


class PurchasedBooks(models.Model):
    user = models.ForeignKey(EludeUser)
    book = models.ForeignKey(Book)
    additional_information = models.TextField()
    time_book_was_bought = models.DateTimeField()


class NewTransactionProcess(models.Model):
    user = models.ForeignKey(EludeUser, default="guest")
    book = models.ManyToManyField(Book)
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify("%s%s" % (self.title, str(self.id)))
        super(NewTransactionProcess, self).save(*args, **kwargs)


