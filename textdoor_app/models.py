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
    book_condition = models.CharField(max_length=25)
    author = models.CharField(max_length=500)
    sales_price = models.CharField(default="0.00", max_length=500)
    publish_date = models.DateTimeField(db_index=True, blank=True, default=datetime.now)
    publish_type = models.CharField(default="Now", max_length=15)
    book_owner = models.ForeignKey(EludeUser, default='')
    slug = models.SlugField(max_length=100)
    book_edition = models.CharField(max_length=100, blank=True)
    book_description = models.CharField(max_length=6000, blank=True, default="")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single_book_description', args=(self.id, self.slug))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = '%s' % slugify(self.title)
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
    cropping = ImageRatioField('book_image', '60x60')

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
    status = models.CharField(max_length=100, default="Applied")


class SoldBooks(models.Model):
    user = models.ForeignKey(EludeUser)
    book = models.ForeignKey(Book)
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


