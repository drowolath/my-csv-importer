from csvImporter import celery_app
from .models import Product

import pandas
import json

@celery_app.task(name="filestore.storeproduct", queue="products")
def slice_csv(path):
    df = pandas.read_csv(path)
    limit = 0
    while limit <= df.shape[0]:
        print(limit, limit+100)
        data = df[limit:limit+100].to_json()
        limit += 100
        data = json.loads(data)
        for item, sku in data['sku'].items():
            product, _ = Product.objects.get_or_create(sku__iexact=sku)
            product.name = data['name'][item]
            product.description = data['description'][item]
            print(product.__dict__)
            product.save()
