import csv
from store.models import Category

def feed_categories():
    Category.objects.all().delete()    
    with open('data/categories.csv') as csv_file:
        csv_dict_reader = csv.DictReader(csv_file, delimiter=';')        
        for item in csv_dict_reader:
            category = Category(name=item['name'], slug=item['slug'])
            category.save()
            print(f'Category created: {category}')

def run():
    feed_categories()