import datetime
from haystack import indexes
from textdoor_app.models import Book


class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='user')
    pub_date = indexes.DateTimeField(model_attr='pub_date')
    title = indexes.CharField(model_attr='title')
    isbn_number = indexes.CharField(model_attr='isbn_number')

    def get_model(self):
        return Book

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())