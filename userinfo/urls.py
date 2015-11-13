__author__ = 'Administrator'

from django.conf.urls import url

import userinfo.views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from . import views

urlpatterns = [
    url(r'^signup/$', userinfo.views.SignUpPageView.as_view(), name='user_registration_page'),
    url(r'^(?P<pk>[0-9]+)/(?P<user_name>.*)/home/$', userinfo.views.UserHomeProfilePage.as_view(),
        name='user_home_profile_page'),
    url(r'^login/$', userinfo.views.LoginView.as_view(), name='login_page'),
    url(r'^(?P<pk>[0-9]+)/(?P<user_name>.*)/new-book-listing/$', userinfo.views.NewBookListingView.as_view(),
        name='new_book_entry_page'),
    url(r'^(?P<pk>[0-9]+)/(?P<user_name>.*)/success-page/$', userinfo.views.SuccessPageView.as_view(),
        name='success_url_page'),
    url(r'^(?P<pk>[0-9]+)/(?P<user_name>.*)/search/result/$', 'userinfo.views.search', name='search_result_page'),
    url(r'^(?P<pk>[0-9]+)/(?P<user_name>.*)/list-of-your-book/$', userinfo.views.ListOfYourBooksView.as_view(),
        name='list_of_your_books'),
    url(r'^(?P<pk>[0-9]+)/(?P<book_id>[0-9]+)/(?P<slug>[-\w\d\ ]+)/$',
    userinfo.views.SingleBookDescriptionView.as_view(), name='single_book_description'),
    url(r'^(?P<pk>[0-9])+/(?P<user_name>.*)/watch-list/$', userinfo.views.WatchListBooksView.as_view(), name='watch_list'),
     url(r'^(?P<pk>[0-9])+/(?P<user_name>.*)/books-out-on-rent/$', userinfo.views.BooksOutOnRentView.as_view(),
        name='books_out_on_rent'),
    url(r'^(?P<pk>[0-9])+/(?P<user_name>.*)/books-you-are-renting/$', userinfo.views.BooksYouAreRentingView.as_view(),
        name='books_your_renting'),
    url(r'^(?P<pk>[0-9])+/(?P<user_name>.*)/trade-history/$', userinfo.views.TradeHistoryView.as_view(),
    name='trade_history')
]
urlpatterns += staticfiles_urlpatterns()
"""
    url(r'^(?P<pk>[0-9])+/(?P<user_name>.*)/order-history/$', userinfo.views.OrderHistoryView.as_view(),
        name='order_history'),


urlpatterns += staticfiles_urlpatterns()"""
