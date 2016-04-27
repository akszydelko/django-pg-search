from django.db.models import Manager

from .query import SearchQuerySet


class ReadOnlyManager(Manager):
    def bulk_create(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def get_or_create(self, *args, **kwargs):
        raise NotImplementedError

    def update_or_create(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError


class ReadOnlySearchManager(ReadOnlyManager):
    """
    Model manager which block editing operations and adds useful search method.
    E.g. Model.objects.search("Foo bar")
    """

    def __init__(self, search_field, title_field=None):
        super(ReadOnlySearchManager, self).__init__()
        self.search_field = search_field
        self.title_field = title_field
        self._queryset_class = SearchQuerySet

    def contribute_to_class(self, cls, name):
        """Called automatically by Django when setting up the model class."""
        if not cls._meta.abstract:
            # Attach this manager as _fts_manager in the model class.
            if not getattr(cls, "_fts_manager", None):
                cls._fts_manager = self

        super(ReadOnlySearchManager, self).contribute_to_class(cls, name)

    def search(self, search_term, **kwargs):
        """Pass through function to search function of SearchQuerySet class."""
        return self.get_queryset().search(search_term, **kwargs)
