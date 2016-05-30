isbn_api = 'ac4e0fb30ab0e1439cd8e378586317fa'
isbn_api_key = 'RJ6ZOHK5'
'''
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser

def desirilize_isbn_number(isbn_value):
    stream = BytesIO(isbn_value)
    data = JSONParser().parse(stream)
    serializer =
    '''
import json


def decode_isbn_value(isbn_value):

    dictionary = json.loads(isbn_value.content)
    return dictionary

