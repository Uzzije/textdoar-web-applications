from elude_web_application.setting_secret import BUYERS_TAX_AND_PROCESSING_FEE, \
    STRIPE_AND_TEXTDOAR_PAYMENT_PROCESSING_FEE, TRANSACTION_FEE, ACTIVATION_CODE_LIST, ACTIVATION_CODE_DIC
from random import randint
from rauth import OAuth2Service

BUYERS_FEE = BUYERS_TAX_AND_PROCESSING_FEE
def get_string_from_list(list):
    word = ','.join(list)
    return word

stripe_token = OAuth2Service(client_secret='sk_test_0nUBiJyARoPOsmheLyUv4Glq',
                             client_id='ca_7bk9PU3cXS93KOuRKMFSerKPMo4pBoMe',
                             name='stripe',
                             authorize_url='https://connect.stripe.com/oauth/authorize',
                             access_token_url='https://connect.stripe.com/oauth/token',
                             base_url='https://connect.stripe.com/')


def application_fee_amount(book_price):
    fees = float(STRIPE_AND_TEXTDOAR_PAYMENT_PROCESSING_FEE) + float(float(TRANSACTION_FEE) * float(book_price)) + \
           float(BUYERS_TAX_AND_PROCESSING_FEE)
    return int(fees*100)


def application_fee_amount_not_for_stripe(book_price):
    fees = float(STRIPE_AND_TEXTDOAR_PAYMENT_PROCESSING_FEE) + float(float(TRANSACTION_FEE) * float(book_price)) + \
           float(BUYERS_TAX_AND_PROCESSING_FEE)
    return str(fees)


def get_activation_code():
    index = randint(0, len(ACTIVATION_CODE_LIST)-1)
    return ACTIVATION_CODE_LIST[index]


def validate_activation_code(user_code_input):
    if user_code_input in ACTIVATION_CODE_LIST:
        # Just double checking
        if user_code_input in ACTIVATION_CODE_DIC:
            return True
    return False


def get_textdoar_commission(book_price):
    fee = float(application_fee_amount_not_for_stripe(book_price)) - float(get_buyers_fee())
    return  fee


def generate_invoice_number(sold_book_id):
    invoice_number = randint(1000, 1999)
    return str(invoice_number) + str(sold_book_id)


def get_buyers_fee():
    return BUYERS_FEE


def get_total_price_of_purchase(book_price):
    return str(float(get_buyers_fee()) + float(book_price))


def convert_str_to_money(string_value):
    return '${:,.2f}'.format(float(string_value))


def card_type(number):
    if len(number) == 13:
        if number[0] == "4":
            return "Visa"
    elif len(number) == 14:
        if number[:2] == "36":
            return "MasterCard"
    elif len(number) == 15:
        if number[:2] in ("34", "37"):
            return "American Express"
    elif len(number) == 16:
        if number[:4] == "6011":
            return "Discover"
    if number[:2] in ("51", "52", "53", "54", "55"):
        return "MasterCard"
    if number[0] == "4":
        return "Visa"
    return "Unknown"