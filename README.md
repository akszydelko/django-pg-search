Django PG Search
================

Minimalistic application with fields, managers etc. for full text search support in PostgreSQL.


### Installation

```bash
pip install django-pg-search
```

Example usage:

```python
class Search(models.Model):
    object_id = models.IntegerField()
    language = models.CharField(max_length=2)
    name = models.CharField(max_length=255, primary_key=True)
    search_term = TSVectorField()

    objects = ReadOnlySearchManager(
        search_field='search_term',
        title_field='name'
    )

    class Meta:
        managed = False
        db_table = 'search_view'
```


### Legal

Copyright (c) 2017, Arkadiusz Szydełko All rights reserved.

Licensed under BSD 3-Clause License
