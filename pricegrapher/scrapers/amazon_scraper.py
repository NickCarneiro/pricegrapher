from django.core.exceptions import FieldError
import re
from pricegrapher.models import Product, Price, Source, ProductSource
from source import Source as Source_Parent
from bs4 import BeautifulSoup as bs
import urllib2
class AmazonSource(Source_Parent):
    source_title = 'amazon'
    amazon_product_url = 'http://www.amazon.com/gp/product/'
    def __init__(self):
        pass
    """
    scrape the product page of the given ASIN
    return false if trouble
    """
    def scrape_product(self, asin):
        try:
            url = self.amazon_product_url + asin
            html = urllib2.urlopen(url).read()
            soup = bs(html)
            title = soup.find('span', id='btAsinTitle')
            title_string = title.text
            print title_string

            price_amount = self.get_price_from_soup(soup)

            description = soup.find('ul', attrs={'style':'list-style-type: disc; margin-left: 25px;'})
            if description is None:
                # maybe it's a book like
                description = soup.find('div', id='postBodyPS')
                if description is not None:
                    description = str(description.renderContents())
                    # maybe it's like this blender B0017XHSAE
            if description is None:
                description = soup.find('ul', attrs={'style': 'list-style-type: disc;'})
                # maybe it's some kind of CD B002BSHWUU
            if description is None:
                description = soup.find('div', attrs={'class': 'productDescriptionWrapper'})
                # maybe it's a digital download like this B008B1VYP0
            if description is None:
                content_divs = soup.findAll('div', attrs={'class': 'content'})
                if len(content_divs) > 1:
                    description = content_divs[1].text.split('ASIN:')[0]
            if description is None:
                description = ''
            product = Product(title=title_string, description=description)
            product.save()
            # associate a source model with this product
            try:
                amazon_source = Source.objects.get(title='amazon')
            except Source.DoesNotExist:
                amazon_source = None

            if amazon_source is None:
                # if there is no amazon source in the database, create one.
                amazon_source = Source(title='amazon', url='http://amazon.com')
                amazon_source.save()
            product_source = ProductSource(product=product, source=amazon_source, local_id=asin)
            product_source.save()
            price_model = Price.objects.create(price=price_amount, product=product, source=amazon_source)
            price_model.save()
            return product
        except Exception as e:
            print e
            return False


    """
    Try to create a new product. If it already exists, return its model.
    If the URL is bad or anything else goes wrong, return False.
    """
    def create(self, url):
        #extract ASIN from url
        asin = self.get_asin_from_url(url)
        if asin is None:
            return False
        else:
            #make sure product doesn't exist
            existing_product = self.get_product_by_source_id(asin)
            if existing_product is not None:
                return existing_product
            product = self.scrape_product(asin)
            return product


    """
    Given any style of amazon product url, return the ASIN
    """
    def get_asin_from_url(self, url):
        # delete all query params
        qpos = url.find('?')
        if qpos != -1:
            url = url[0: qpos]
        segments = url.split('/')
        for seg in segments:
            if len(seg) == 10 and re.match('^[A-Z0-9_]+$', seg) is not None:
                if prev_seg in ['product', 'asin', 'dp', 'glance']:
                    return  seg
            prev_seg = seg
        return None

    def get_product_by_source_id(self, source_id):
        try:
            product_source_model = ProductSource.objects.get(local_id=source_id)
            product = product_source_model.product
            return product
        except Product.DoesNotExist:
            return None
        except ProductSource.DoesNotExist:
            return None
        except FieldError:
            return None

    def add_new_price(self, product):
        # hit amazon and get the price
        product_source = ProductSource.objects.get(product=product)
        asin = product_source.local_id
        if asin is not None:
            url = self.amazon_product_url + asin
            html = urllib2.urlopen(url).read()
            soup = bs(html)
            price = self.get_price_from_soup(soup)
            if price is None:
                return False
            price_model = Price.objects.create(price=price, product=product, source=product_source.source)
            price_model.save()
            return price_model
        else:
            return False

    """
    return a price int like 1099 if something is $10.99
    or return false
    """
    def get_price_from_soup(self, soup):
        try:
            price_string = soup.find('b', attrs={'class':'priceLarge'}).text
            price_amount = int(float(price_string.replace('$', '')) * 100)
            if price_amount is None:
                return False
            else:
                return price_amount
        except Exception:
            return False



