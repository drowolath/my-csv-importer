from csvImporter import celery_app
from .models import Product

import json


@celery_app.task(name="filestore.storeproduct", queue="products")
def store_products(data):
    """data is the result of.to_json()
    on a pandas dataframe
    """
    data = json.loads(data)
    for item, sku in data['sku'].items():
        product, _ = Product.objects.get_or_create(sku__iexact=sku)
        product.name = data['name'][item]
        product.description = data['description'][item]
        product.save()
        
