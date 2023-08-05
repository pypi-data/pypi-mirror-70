from collections import namedtuple

Filter = namedtuple('Filter', 'field lookups transform_value')
Relation = namedtuple('Relation', 'field resource_name many primary_key_name required')
GenericRelation = namedtuple('GenericRelation', 'field related many required')
CustomField = namedtuple('CustomField', 'name callback')
