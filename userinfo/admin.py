from django.contrib import admin
from userinfo.models import Book, Watchlist

# Register your models here.


class BookAdmin(admin.ModelAdmin):
    pass
admin.site.register(Book)
admin.site.register(Watchlist)