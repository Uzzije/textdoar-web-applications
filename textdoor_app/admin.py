from django.contrib import admin
from textdoor_app.models import Book, Watchlist, EludeUserAddress, EludeUser, BookImage
from image_cropping import ImageCroppingMixin
# Register your models here.


class BookAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass
admin.site.register(Book)
admin.site.register(Watchlist)
admin.site.register(EludeUserAddress)
admin.site.register(EludeUser)
admin.site.register(BookImage)
