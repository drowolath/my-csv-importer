from csvImporter import celery_app
from .models import Product

import pandas
import json

@celery_app.task(name="filestore.storeproduct", queue="products")
def slice_csv(path):
    print(path)
    df = pandas.read_csv(path)
    limit = 0
    while limit <= df.shape[0]:
        print(limit, limit+100)
        data = df[limit:limit+100].to_json()
        limit += 100
        data = json.loads(data)
        for item, sku in data['sku'].items():
            product, created = Product.objects.get_or_create(sku__iexact=sku)
            if created:
                product.name = data['name'][item]
                product.description = data['description'][item]
                product.save()
            else:
                Product.objects.filter(sku=product.sku).update(
                    name=data['name'][item],
                    description=data['description'][item]
                )
