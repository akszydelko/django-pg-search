"""
Minimalistic application with fields, managers etc. for full text search support in PostgreSQL.

Inspired by: https://github.com/linuxlewis/djorm-ext-pgfulltext
"""

FTS_CONFIGURATIONS = {
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'fi': 'finnish',
    'fr': 'french',
    'de': 'german',
    'hu': 'hungarian',
    'it': 'italian',
    'no': 'norwegian',
    'nb': 'norwegian',
    'nn': 'norwegian',
    'pt': 'portuguese',
    'ro': 'romanian',
    'ru': 'russian',
    'simple': 'simple',
    'es': 'spanish',
    'sv': 'swedish',
    'tr': 'turkish',
}

FTS_CONFIGURATIONS.update({v: v for v in FTS_CONFIGURATIONS.values()})
