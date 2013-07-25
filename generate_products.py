#!/usr/bin/env python

#
# Use this while we're still faffing about with models to generate a ten of
# random products each with ten random prices "from Amazon" very quickly.
# Start a shell with `./manage.py shell` and `import generate_products`.
#

from pricegrapher.models import *
import datetime
import random

def name():
  colors = ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Indigo', 'Violet']
  shapes = ['Triangle', 'Square', 'Pentagon', 'Hexagon', 'Septagon', 'Octagon']
  return ('%s %s #%d' %
          (''.join(random.sample(colors, 1)),
           ''.join(random.sample(shapes, 1)),
           random.randint(0, 255)))

def local():
  array = range(ord('0'), ord('9')+1) + range(ord('A'), ord('Z')+1)
  new_local = []
  while len(new_local) < 10:
    new_local += chr(random.sample(array, 1)[0])
  return new_local

def date():
  today = datetime.date.today()
  return datetime.date(today.year, 10,
                       random.randint(1, 30))

def price():
  return '%.2f' % (20.0 * random.uniform(0.5, 1.5))

# Create a product source.
amazon = Source(title='Amazon', url='http://amazon.com/')
amazon.save()

# Generate a random product with some random prices.
def product():
  p = Product(title=name()); p.save()
  ProductSource(product=p, source=amazon, local_id=local()).save()
  for i in xrange(10):
    random_date = date()
    Price(product=p, source=amazon, price=price(), datetime=random_date).save()

for i in xrange(10): product()

# Make sure shit works by dumping everything we added.
products = Product.objects.all()
print 'Products:'; print products

prices = Price.objects.filter(product=products[0])
print 'Prices for P#1:'; print prices

