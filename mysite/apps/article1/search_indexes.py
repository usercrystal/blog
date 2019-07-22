from haystack import indexes
from .models import ArticlePost1

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return ArticlePost1

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(status='q')
