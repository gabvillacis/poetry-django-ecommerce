import csv
from store.models import Product, Category

def feed_products():
    Product.objects.all().delete()    
    with open('data/products.csv') as csv_file:
        csv_dict_reader = csv.DictReader(csv_file, delimiter=';')        
        for item in csv_dict_reader:
            product = Product(  name=item['name'],
                                description=item['description'],
                                slug=item['slug'],                                
                                image= 'images/' + item['image'],
                                price=item['price'],
                                is_active=item['is_active'])
            product.save()
            category = Category.objects.get(slug=item['category_slug'])
            product.categories.add(category)
            product.save()
            print(f'Product created: {product}')

def run():
    feed_products()