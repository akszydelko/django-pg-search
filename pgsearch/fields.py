from django.db import models

from .lookups import FullTextLookupStartsWith


class TSVectorField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['default'] = ''
        kwargs['editable'] = False
        kwargs['serialize'] = False
        super(TSVectorField, self).__init__(*args, **kwargs)

    def db_type(self, *args, **kwargs):
        return 'tsvector'

    def get_db_prep_lookup(self, lookup_type, value, connection, prepared=False):
        return self.get_prep_lookup(lookup_type, value)


TSVectorField.register_lookup(FullTextLookupStartsWith)
