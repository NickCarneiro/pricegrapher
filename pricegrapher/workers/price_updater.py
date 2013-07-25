import sys
PROJECT_PATH = '/home/burt/development/pricegrapher/pg/'
sys.path.append(PROJECT_PATH)
from django.db.models.base import Model
from pricegrapher.models import Product
from pricegrapher.scrapers.amazon_scraper import AmazonSource
import time
all_products = Product.objects.all()
for product in all_products:
    sources = product.sources.all()
    #add price for this product
    for source in sources:
        # source titles should be all lowercase and match the name of the class file name
        # all the classes should implement Source for the polymorphism to work here
        # eg amazon, newegg, titlenine
        source_class = source.title
        source_instance = AmazonSource() # TODO: change this line to dynamically instantiate correct source
        price_model = source_instance.add_new_price(product)
        if isinstance(price_model, Model):
            print 'New price for ' + product.title + ': ' + str(price_model.price)
        else:
            print "Couldn't get price for " + product.source_id
        time.sleep(1)
