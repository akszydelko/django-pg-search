from django.db.models import Lookup
from psycopg2._psycopg import adapt


class FullTextLookupStartsWith(Lookup):
    """
    This lookup scans for full text index entries that BEGIN with a given phrase, like:

    Model.objects.filter(search_field__fts_startswith=['Foo', 'Bar'])

    will get translated to ts_query('Foo:* & Bar:*')
    """
    lookup_name = 'fts_startswith'

    @staticmethod
    def __quotes(word_list):
        return ['{}'.format(adapt(x.replace('\\', ''))) for x in word_list]

    def __transform(self, word_list):
        return ['{}:*'.format(x) for x in self.__quotes(word_list)]

    def as_sql(self, qn, connection):
        lhs, lhs_params = qn.compile(self.lhs)
        rhs, rhs_params = self.process_rhs(qn, connection)

        if isinstance(rhs_params, str):
            rhs_params = [rhs_params]

        # Basic query
        cmd = '{} @@ to_tsquery(unaccent(%s))'.format(lhs)
        rest = (' & '.join(self.__transform(rhs_params)),)

        return cmd, rest
