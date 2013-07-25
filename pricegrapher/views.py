import json
import locale
import re
import urllib
import urlparse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.template.context import Context
import unicodedata

from pricegrapher.forms import UrlForm
from pricegrapher.models import Product, Price
from pricegrapher.scrapers.amazon_scraper import AmazonSource

def sandbox(request):
    products = Product.objects.order_by('-date_added');
    template = loader.get_template('sandbox.html')
    context = Context({
        'products': products
    })
    return HttpResponse(template.render(context))

def index(request):
    template = loader.get_template('index.html')
    context = Context({})
    return HttpResponse(template.render(context))

def lookup(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)

        if form.is_valid():
            fields = form.cleaned_data
            source = AmazonSource()
            product = source.create(fields['productUrl'])
            if product:

                safe_url = url_fix(unicode(product.title))
                response_data = {
                    'redirectUrl': '/products/' + str(product.id) + '/' + safe_url
                }
            else:
                response_data = {
                    'error': 'Could not find a product at that URL.'
                }
        else:
            response_data = {
                'error': 'The URL was invalid.'
            }
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

def product(request, pid):
    product = get_object_or_404(Product, pk=pid)

    # Convert a Python datetime into something Google Charts can handle.
    def js(py): return 'Date(%s, %s, %s)' % (py.year, py.month, py.day)

    # Wrangle the data into the right format for Google Charts.
    data = {'cols': [{'type': 'date'}, {'type': 'number'}, {'type': 'string'}],
            'rows': map(lambda x: {'c': [{'v': y} for y in x]},
                        [(js(p.datetime), float(p.price / 100.0), str(p.source.title))
                         for p in Price.objects.filter(product=product)])}
    # look up latest price
    prices = Price.objects.filter(product=product)
    try:
        latest_price = prices[len(prices) - 1].price
        formatted_price = money_format(latest_price)
    except AssertionError:
        formatted_price = 'No price found.'
    return render(request, 'product.htm', {'product': product, 'data': data, 'price': formatted_price})


def url_fix(string):
    return re.sub(r'[-\s]+', '-',
        unicode(
            re.sub(r'[^\w\s-]', '',
                unicodedata.normalize('NFKD', string)
                .encode('ascii', 'ignore'))
            .strip()
            .lower()))

def money_format(value):
    return locale.currency(value / 100.0)

