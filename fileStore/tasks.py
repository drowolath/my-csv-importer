from csvImporter import celery_app
from .models import Product

import pandas
import json

@celery_app.task(name="filestore.storeproduct", queue="products")
def process(data):
    for item, sku in data['sku'].items():
        sku = sku.lower()
        name = data['name'][item]
        description = data['description'][item]
        active = bool(
            int(data.get('active', '0')[item])
        )
        product, created = Product.objects.get_or_create(sku=sku)
        if created:
            product.name = name
            product.description = description
            product.active = active
            product.save()
        else:
            Product.objects.filter(sku=product.sku).update(
                name=name,
                description=description,
                active=active
            )


@celery_app.task(name="filestore.slice_csv", queue="slicer")
def slice_csv(path):
    df = pandas.read_csv(path)
    limit = 0
    while limit <= df.shape[0]:
        data = df[limit:limit+100].to_json()
        limit += 100
        data = json.loads(data)
        process.delay(data)
