import json

from django.test import TestCase

from tastypie.test import ResourceTestCase

from django.template.defaultfilters import slugify

from django.core.urlresolvers import reverse

from lfs.catalog.models import Product
from lfs.catalog.models import Property
from lfs.catalog.models import PropertyGroup
from lfs.catalog.models import PropertyOption
from lfs.catalog.models import ProductAccessories
from lfs.catalog.models import ProductPropertyValue
from lfs.catalog.models import ProductsPropertiesRelation

from lfs_rest.api import ProductResource

# http://django-tastypie.readthedocs.org/en/latest/testing.html
# http://stackoverflow.com/questions/971667/django-orm-how-to-view-or-log-the-executed-query
# http://dabapps.com/blog/logging-sql-queries-django-13/

class ProductTestCase(ResourceTestCase):
    """
    """

    url = "/api/product/"

    def setUp(self):
        """
        """
        super(ProductTestCase, self).setUp()

    def test_create(self):
        rr = self.client.get(self.url)
        result = json.loads(rr.content)
        self.assertEqual(result['objects'],[])
        
        data = dict(
            sku = "code",
            name = "A product",
            price = 10.0,
            slug = slugify("A product")
        )

        rr = self.api_client.post(self.url, data=data)
        self.assertHttpCreated(rr)

        prod = Product.objects.get(sku=data['sku'])
        self.assertEqual(prod.name, data['name'])
        self.assertEqual(prod.price, data['price'])
        self.assertEqual(prod.slug, data['slug'])

    def test_get(self):
        data = dict(
            slug="product-1",
            price=5,
            active=True,
            sku = "sku",
            name = "Product 1"
        )
        prod = Product.objects.create(**data)

        rr = self.api_client.get(self.url, data=dict(sku=prod.sku))

        self.assertValidJSONResponse(rr)

        item = json.loads(rr.content)['objects'][0]
        
        self.assertEqual(data['name'],item['name'])
        self.assertEqual(data['price'],item['price'])
        self.assertEqual(data['active'],item['active'])

    def test_update(self):
        data = dict(
            sku = "code",
            name = "A product",
            price = 10.0,
            slug = slugify("A product")
        )

        prod = Product.objects.create(**data)
        new_data = dict(
            name = "A new name for this",
        )
        url = "%s%s/" % (self.url, prod.id)
        rr = self.api_client.put(url, data=new_data)
        prod = Product.objects.get(sku=data['sku'])
        self.assertEqual(prod.name, new_data['name'])

    def test_delete(self):
        data = dict(
            sku = "code",
            name = "A product",
            price = 10.0,
            slug = slugify("A product")
        )
        prod = Product.objects.create(**data)
        url = "%s%s/" % (self.url, prod.id)
        rr = self.api_client.delete(url)
        try:
            Product.objects.get(sku=data['sku'])
        except Product.DoesNotExist:
            pass

    


# Size: s, m, l 
# Variants
# ########
# [
#     {
#         "sku": "4711",
#         "variants": [
#             {
#                 "properties": {
#                     "color": {
#                         "title": "Color",
#                         "unit": "",
#                         "type": "select",
#                         "options": [{
#                             "position": 10,
#                             "name": "red",
#                             "price": 0.0,
#                         }]
#                     }
#                 },
#                 "sku": "4711-1",
#             }
#         ]
#     }
# ]
# Properties
# ##########  
# [
#     {
#         "name": "color",
#         "title": "Color",
#         "unit": "",
#         "type": "select",
#         "options": [{
#             "position": 10,
#             "name": "red",
#             "price": 0.0,
#         }]
       
#     },
#     {
#         "name": "size",
#         "title": "Size",
#         "unit": "",
#         "type": "select",
#         "options": [
#             {
#                 "position": 10,
#                 "name": "m",
#                 "price": 0.0,
#             }
#         ]       
#     },
# ]