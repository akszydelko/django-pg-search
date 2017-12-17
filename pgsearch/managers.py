from django.db.models.manager import BaseManager

from .query import SearchQuerySet


class ReadOnlyManager(object):
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


class ReadOnlySearchManager(ReadOnlyManager, BaseManager.from_queryset(SearchQuerySet)):
    """
    Model manager which block editing operations and adds search method.
    E.g. Model.objects.search("Foo bar")
    """

    def __init__(self, search_field, title_field=None):
        super(ReadOnlySearchManager, self).__init__()
        self.search_field = search_field
        self.title_field = title_field

    def contribute_to_class(self, cls, name):
        """Called automatically by Django when setting up the model class."""
        if not cls._meta.abstract:
            # Attach this manager as _fts_manager in the model class.
            if not getattr(cls, "_fts_manager", None):
                cls._fts_manager = self

        super(ReadOnlySearchManager, self).contribute_to_class(cls, name)
