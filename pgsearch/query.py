from django.db.models import QuerySet
from psycopg2._psycopg import adapt


class BaseQuerySet(QuerySet):
    @staticmethod
    def qn(name):
        """
        Quote name function definition was taken from
        django.db.backends.postgresql_psycopg2.operations.DatabaseOperations#quote_name
        as we plan to use only PostgreSQL so far and other methods of gathering this function required too much.
        """
        if name.startswith('"') and name.endswith('"'):
            return name  # Quoting once is enough.
        return '"%s"' % name


class SearchQuerySet(BaseQuerySet):
    @property
    def manager(self):
        return self.model._fts_manager

    @staticmethod
    def __transform(word_list):
        return [x.strip() + ":*" for x in filter(lambda x: x.strip(), word_list)]

    def search(self, search_term, using=None, rank_ordering=True, rank_normalization=32,
               fts_language="english", headline_field=None):
        """Use full text search utilities for looking through all objects."""
        qs = self
        qn = self.qn

        if using is not None:
            qs = qs.using(using)

        if search_term:
            if isinstance(search_term, basestring):
                search_term = search_term.split(" ")

            ts_query = ("to_tsquery('%s', unaccent(%s))" % (
                fts_language,
                adapt((" & ".join(self.__transform(search_term))).encode('utf-8'))
            )).decode('utf-8')

            search_field_name = "%s.%s" % (
                qn(self.model._meta.db_table),
                qn(self.manager.search_field)
            )

            where = "%s @@ %s" % (search_field_name, ts_query)
            select_dict, order = {}, []

            if rank_ordering:
                select_dict['rank'] = "ts_rank(%s, %s, %d)" % (
                    search_field_name,
                    ts_query,
                    rank_normalization
                )
                order = "-rank"

            if headline_field:
                select_dict[headline_field] = "ts_headline('%s', %s, %s)" % (
                    fts_language,
                    "%s.%s" % (qn(self.model._meta.db_table), qn(headline_field)),
                    ts_query
                )

            qs = qs.extra(select=select_dict, where=[where], order_by=[order])

        return qs
