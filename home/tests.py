# -*- coding: utf-8 -*-
from django.db import models
from django.test import TestCase
from dbindexer.api import register_index
from dbindexer.lookups import StandardLookup
from dbindexer.resolver import resolver
from djangotoolbox.fields import ListField
from datetime import datetime
import re
from home.models import Category

# TODO: add test for foreign key with multiple filters via different and equal paths
# to do so we have to create some entities matching equal paths but not matching
# different paths
class IndexedTest(TestCase):
    def setUp(self):
        self.backends = list(resolver.backends)
        resolver.backends = []
        resolver.load_backends(('dbindexer.backends.BaseResolver',
                      'dbindexer.backends.FKNullFix',
#                      'dbindexer.backends.InMemoryJOINResolver',
                      'dbindexer.backends.ConstantFieldJOINResolver',
        ))
        self.register_indexex()
        Category(name=u'Hồng Hạc').save()

    def tearDown(self):
        resolver.backends = self.backends

    def register_indexex(self):
        register_index(Category, {
            'name': ('iexact', 'endswith', 'istartswith', 'iendswith', 'contains',
                     'icontains', re.compile('^i+', re.I), re.compile('^I+'),
                     re.compile('^i\d*i$', re.I)),
        })

    # TODO: add tests for created indexes for all backends!
#    def test_model_fields(self):
#        field_list = [(item[0], item[0].column)
#                       for item in Indexed._meta.get_fields_with_model()]
#        print field_list
#        x()
        # in-memory JOIN backend shouldn't create multiple indexes on the foreignkey side
        # for different paths or not even for index definition on different models. Test this!
        # standard JOIN backend should always add extra fields to registered model. Test this!
    def test_contains(self):
        self.assertEqual(1, len(Category.objects.all().filter(name__contains=u'Hồng')))

