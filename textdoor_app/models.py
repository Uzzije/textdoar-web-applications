from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from image_cropping import ImageRatioField
from django.utils.timezone import now


class EludeUserAddress(models.Model):
    address = models.CharField(default=None, max_length=600)
    city = models.CharField(default=None, max_length=600)
    state = models.CharField(default=None, max_length=600)
    zip_code = models.CharField(default=None, max_length=600)
    current_shipping_address = models.BooleanField(default=False)


class StripeData(models.Model):
    token_type = models.CharField(default=None, max_length=1000)
    stripe_publishable_key= models.CharField(default=None, max_length=1000)
    scope = models.CharField(default=None, max_length=1000)
    stripe_user_id = models.CharField(default=None, max_length=1000)
    refresh_token = models.CharField(default=None, max_length=1000)
    access_token = models.CharField(default=None, max_length=1000)


class PaymentCardData(models.Model):
    customer_id = models.CharField(max_length=1000, default="No customer ID")
    is_user_current_option = models.BooleanField(default=False)
    address = models.CharField(max_length=1000, default="No Address")
    address_state = models.CharField(max_length=100, default="No State")
    address_country = models.CharField(max_length=100, default="No Country")
    address_zip_code = models.CharField(max_length=100, default="No Zip Code")
    exp_month = models.CharField(max_length=10, default="No exp month")
    exp_year= models.CharField(max_length=10, default="No exp year")
    last_4_of_card = models.CharField(max_length=10, default="No last Four")
    card_brand = models.CharField(max_length=100, default="No card brand")
    funding_type = models.CharField(max_length=100, default="No funding type")
    created_date = models.DateTimeField(default=now)


class BankAccountData(models.Model):
    name_on_bank_account = models.CharField(max_length=1000)
    bank_token_id = models.CharField(max_length=100)


class EludeUser(models.Model):
    username = models.OneToOneField(User)
    college_attending = models.CharField(max_length=254)
    new_user = models.BooleanField(default=True)
    address = models.ManyToManyField(EludeUserAddress)
    stripe_data = models.ForeignKey(StripeData, blank=True, null=True)
    stripe_account_activated = models.BooleanField(default=False)
    payment_card_info = models.ManyToManyField(PaymentCardData, blank=True)
    phone_number = models.CharField(default="000-000-0000", max_length=15)


    def __str__(self):
        return self.username.username


class Book(models.Model):
    title = models.CharField(db_index=True, max_length=500)
    isbn_number = models.CharField(db_index=True, max_length=500)
    book_condition = models.CharField(max_length=25)
    author = models.CharField(max_length=500)
    sales_price = models.CharField(default="0.00", max_length=500)
    publish_date = models.DateTimeField(db_index=True, blank=True, default=now)
    publish_type = models.CharField(default="Now", max_length=15)
    book_owner = models.ForeignKey(EludeUser, default='')
    slug = models.SlugField(max_length=100)
    book_edition = models.CharField(max_length=100, blank=True)
    book_description = models.CharField(max_length=6000, blank=True, default="")
    book_is_sold = models.BooleanField(default=False)

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
    buyer = models.ForeignKey(EludeUser, related_name='buyer', blank=True, null=True)
    seller = models.ForeignKey(EludeUser, related_name='seller', blank=True, null=True)
    book = models.ForeignKey(Book)
    time_book_was_sold = models.DateTimeField(default=now)
    delivered_to_buyer = models.BooleanField(default=False)
    order_number = models.CharField(default="00000", blank=False, max_length=1000)


class NewTransactionProcess(models.Model):
    user = models.ForeignKey(EludeUser, default="guest")
    book = models.ManyToManyField(Book)
    slug = models.SlugField()
    date = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify("%s%s" % (self.title, str(self.id)))
        super(NewTransactionProcess, self).save(*args, **kwargs)


class StudentFeedBacks(models.Model):
    feed_back = models.CharField(max_length=2000, blank=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    topic = models.CharField(max_length=36, blank=True, null=True)


class BooksStudentsRequested(models.Model):
    name_of_book = models.CharField(max_length=100, blank=True)
    isbn_number = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)