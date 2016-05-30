__author__ = 'Administrator'

from django.conf.urls import url

import textdoor_app.views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^signup/$', textdoor_app.views.SignUpPageView.as_view(), name='user_registration_page'),
    url(r'^(?P<user_name>.*)/home/$', textdoor_app.views.UserHomeProfilePage.as_view(),
        name='user_home_profile_page'),
    url(r'^login/$', textdoor_app.views.LoginViews.as_view(), name='login_page'),
    url(r'^(?P<user_name>.*)/new-book-listing/$', textdoor_app.views.NewBookListingView.as_view(),
        name='new_book_entry_page'),
    url(r'^(?P<user_name>.*)/success-page/$', textdoor_app.views.SuccessPageView.as_view(),
        name='success_url_page'),
    url(r'^(?P<user_name>.*)/search/result/$', textdoor_app.views.SearchResultView.as_view(),
        name='search_result_page'),
    url(r'^(?P<user_name>.*)/list-of-your-book/$', textdoor_app.views.ListOfYourBooksView.as_view(),
        name='list_of_your_books'),
    url(r'^(?P<book_id>[0-9]+)/(?P<slug>[-\w\d\ ]+)/$',textdoor_app.views.SingleBookDescriptionView.as_view(),
        name='single_book_description'),
    url(r'^(?P<user_name>.*)/watch-list/$', textdoor_app.views.WatchListBooksView.as_view(), name='watch_list'),
    url(r'^$', textdoor_app.views.TextDoorHomePageView.as_view(), name='home_page'),
    url(r'^logout/$', textdoor_app.views.LogoutView.as_view(), name='logout'),
    url(r'^(?P<user_name>.*)/cart/$', textdoor_app.views.CartView.as_view(), name='cart_page'),
    url(r'^(?P<user_name>.*)/account/address/$', textdoor_app.views.AddressView.as_view(), name='address_entry_page'),
    url(r'^(?P<user_name>.*)/account/$', textdoor_app.views.AccountView.as_view(), name='account_page'),
    url(r'^payment/$', textdoor_app.views.PaymentView.as_view(), name='payment_page'),
    url(r'^(?P<user_name>.*)/isbn-finder/$', textdoor_app.views.ISBNView.as_view(), name='isbn_entry_page'),
    url(r'^payment-signup-confirmation/$', textdoor_app.views.StripeConnectionConfirmationView.as_view(),
        name='stripe_connection_confirmation_page'),
    url(r'^(?P<user_name>.*)/new-book-list-confirmation/$', textdoor_app.views.ListBookConfirmationView.as_view(),
        name='list_book_confirmation_page'),
    url(r'^(?P<user_name>.*)/pay-with-saved-card/$', textdoor_app.views.SavedCreditCardPaymentView.as_view(),
        name='saved_page_confirmation_page'),
    url(r'^(?P<user_name>.*)/change-password-page/$', textdoor_app.views.ChangePasswordView.as_view(),
        name='change_password_page'),
    url(r'^(?P<user_name>.*)/order-history/$', textdoor_app.views.OrderHistoryView.as_view(),
        name='order_history'),
    url(r'^(?P<user_name>.*)/payment-card-details/$', textdoor_app.views.PaymentCardDetailView.as_view(),
        name='saved_card_page'),
    url(r'^(?P<user_name>.*)/error-page-view/$', textdoor_app.views.ErrorPageViewForStripe.as_view(),
        name='error_page_for_stripe'),
    url(r'^(?P<user_name>.*)/account-activation/$', textdoor_app.views.AccountActivationView.as_view(),
        name='user_activation_page'),
    url(r'^buying-information/$', textdoor_app.views.BuyingInformationView.as_view(),
        name='buying_a_textbook_info_page'),
    url(r'^selling-information/$', textdoor_app.views.SellingInformationView.as_view(),
        name='selling_a_textbook_info_page'),
    url(r'^textdoar-FAQ/$', textdoor_app.views.FAQView.as_view(),
        name='faq_page'),
    url(r'^contact-us/$', textdoor_app.views.ContactUSView.as_view(),
        name='contact_us_page'),
    url(r'^about-us/$', textdoor_app.views.AboutUSView.as_view(),
        name='about_us_page'),
    url(r'^term-and-condition-page/$', textdoor_app.views.TermAndConditionView.as_view(),
        name='term_and_condition_page'),
    url(r'^launch-page-sign-up/$', textdoor_app.views.LaunchPageView.as_view(),
        name='launch_page'),
    url(r'^un-subscribe-page/$', textdoor_app.views.UnsubscribePageView.as_view(),
        name='unsubscribe_page'),

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
