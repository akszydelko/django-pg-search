import re

from django.db.models import QuerySet
from psycopg2._psycopg import adapt

from . import FTS_CONFIGURATIONS


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
        return '"{}"'.format(name)

    qn.queryset_only = True


class SearchQuerySet(BaseQuerySet):
    @property
    def manager(self):
        return self.model._fts_manager

    def __startswith(self, word_list):
        return ['{}:*'.format(x.strip()) for x in filter(lambda x: x.strip(), word_list)]

    __startswith.queryset_only = True

    def __unaccent(self, term):
        return 'unaccent({})'.format(term)

    __unaccent.queryset_only = True

    def __get_tsquery(self, term, config, join_by, startswith, unaccent=True):
        operator = ' {} '.format(join_by)
        query = self.__startswith(term) if startswith else term
        query = adapt(operator.join(query))
        return ("to_tsquery('{}', {})".format(
            config,
            self.__unaccent(query) if unaccent else query
        ))

    __get_tsquery.queryset_only = True

    def search(self, search_term, using=None, rank_ordering=True, rank_function='ts_rank', rank_normalization=32,
               fts_language="english", include_simple=True, join_by="&", startswith=True, divide_by_title_length=False,
               headline_field=None, headline_lang_simple=False):
        """Use full text search utilities for looking through all objects."""
        qs = self

        if using is not None:
            qs = qs.using(using)

        if search_term:
            if isinstance(search_term, str):
                search_term = [x for x in re.sub('[\W-]+', ' ', search_term, flags=re.UNICODE).split(' ') if x]

            fts_language = FTS_CONFIGURATIONS.get(fts_language, 'simple')
            ts_query = self.__get_tsquery(search_term, fts_language, join_by, startswith)

            if include_simple and fts_language != 'simple':
                ts_query += ' || ' + self.__get_tsquery(search_term, 'simple', join_by, startswith)

            ts_query = '({})'.format(ts_query)

            search_field_name = '{}.{}'.format(
                self.qn(self.model._meta.db_table),
                self.qn(self.manager.search_field)
            )

            where = '{} @@ {}'.format(search_field_name, ts_query)
            select_dict, order = {}, []

            if rank_ordering:
                select_dict['rank'] = '{}({}, {}, {})'.format(
                    rank_function,
                    search_field_name,
                    ts_query,
                    '|'.join(rank_normalization) if isinstance(rank_normalization,
                                                               (list, tuple)) else rank_normalization
                )
                order = '-rank'

                if divide_by_title_length and self.manager.title_field:
                    select_dict['rank'] += '/length({}.{})'.format(
                        self.qn(self.model._meta.db_table),
                        self.qn(self.manager.title_field)
                    )

                select_dict['rank'] = '({})'.format(select_dict['rank'])

            if headline_field:
                headline_lang = "simple" if headline_lang_simple else fts_language
                select_dict[headline_field] = "ts_headline('{}', {}, {})".format(
                    headline_lang,
                    '{}.{}'.format(self.qn(self.model._meta.db_table), self.qn(headline_field)),
                    self.__get_tsquery(search_term, headline_lang, join_by, startswith, unaccent=False)
                )

            qs = qs.extra(select=select_dict, where=[where], order_by=[order])

        return qs
