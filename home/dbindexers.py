from home.models import Category
from dbindexer.lookups import StandardLookup
from dbindexer.api import register_index
import re

register_index(Category, {
            'name': ('iexact', 'endswith', 'istartswith', 'iendswith', 'contains',
                     'icontains', re.compile('^i+', re.I), re.compile('^I+'),
                     re.compile('^i\d*i$', re.I)),
        })