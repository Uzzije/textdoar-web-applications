__author__ = 'Administrator'

from django.conf.urls import url

import textdoor_app.views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from . import views

urlpatterns = [
    url(r'^signup/$', textdoor_app.views.SignUpPageView.as_view(), name='user_registration_page'),
    url(r'^(?P<pk>[0-9]+)/(?P<user_name>.*)/home/$', textdoor_app.views.UserHomeProfilePage.as_view(),
        name='user_home_profile_page'),
    url(r'^login/$', textdoor_app.views.LoginView.as_view(), name='login_page'),
    url(r'^(?P<pk>[0-9]+)/(?P<user_name>.*)/new-book-listing/$', textdoor_app.views.NewBookListingView.as_view(),
        name='new_book_entry_page'),
    url(r'^(?P<pk>[0-9]+)/(?P<user_name>.*)/success-page/$', textdoor_app.views.SuccessPageView.as_view(),
        name='success_url_page'),
    url(r'^(?P<pk>[0-9]+)/(?P<user_name>.*)/search/result/$', textdoor_app.views.SearchView.as_view(),
        name='search_result_page'),
    url(r'^(?P<pk>[0-9]+)/(?P<user_name>.*)/list-of-your-book/$', textdoor_app.views.ListOfYourBooksView.as_view(),
        name='list_of_your_books'),
    url(r'^(?P<pk>[0-9]+)/(?P<book_id>[0-9]+)/(?P<slug>[-\w\d\ ]+)/$',
    textdoor_app.views.SingleBookDescriptionView.as_view(), name='single_book_description'),
    url(r'^(?P<pk>[0-9])+/(?P<user_name>.*)/watch-list/$', textdoor_app.views.WatchListBooksView.as_view(), name='watch_list'),
     url(r'^(?P<pk>[0-9])+/(?P<user_name>.*)/books-out-on-rent/$', textdoor_app.views.BooksOutOnRentView.as_view(),
        name='books_out_on_rent'),
    url(r'^(?P<pk>[0-9])+/(?P<user_name>.*)/books-you-are-renting/$', textdoor_app.views.BooksYouAreRentingView.as_view(),
        name='books_your_renting'),
    url(r'^(?P<pk>[0-9])+/(?P<user_name>.*)/trade-history/$', textdoor_app.views.TradeHistoryView.as_view(),
    name='trade_history'),
    url(r'^$', textdoor_app.views.TextDoorHomePageView.as_view(), name='home_page')
]
urlpatterns += staticfiles_urlpatterns()
"""
    url(r'^(?P<pk>[0-9])+/(?P<user_name>.*)/order-history/$', textdoor_app.views.OrderHistoryView.as_view(),
        name='order_history'),


urlpatterns += staticfiles_urlpatterns()"""
