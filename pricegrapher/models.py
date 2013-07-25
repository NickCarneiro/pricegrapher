from django.contrib.auth.models import User
from django.db import models
from datetime import date

# Sources of products: Amazon.com, etc.
class Source(models.Model):
    title = models.CharField(max_length=300)
    url = models.CharField(max_length=2000)

    def __unicode__(self):
        return self.title


# Products: the things whose prices we're tracking.
class Product(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)
    # a product can be found at a multiple stores, and a store has multiple products
    sources = models.ManyToManyField(Source)
    date_added = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.title


# Maps products to sources with an additional identifier.
class ProductSource(models.Model):
    product = models.ForeignKey(Product)
    source = models.ForeignKey(Source)

    # The local identifier: ASIN, SKU, etc.
    local_id = models.TextField()

    def __unicode__(self):
        return 'P#%d @ %s' % (self.product.pk, self.source.title)


# Price updates for products at specific sources.
class Price(models.Model):
    product = models.ForeignKey(Product)
    source = models.ForeignKey(Source)
    # store prices as integers
    # eg, $25.00 = 2500
    price = models.IntegerField()
    datetime = models.DateField(default=date.today())

    def __unicode__(self):
        return 'P#%d @ $%s' % (self.product.pk, self.price / 100.0)


# Keywords for products. (Not implemented.)
# TODO: Normalize this a bit better.
# TODO: Model keyword hierarchy.
class Keyword(models.Model):
    product = models.ForeignKey(Product)
    keyword = models.CharField(max_length=50)

    def __unicode__(self):
        return self.keyword


# Watchlists of products by users. (Not implemented.)
# TODO: Implement the User model.
class WatchList(models.Model):
    user = models.ForeignKey(User)
    private = models.BooleanField()
    title = models.CharField(max_length=500)
    products = models.ManyToManyField(Product)

