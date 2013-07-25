# For a fresh install, boostrap all the sources
from models import Product

# Amazon
amazon = Product.objects.create(title="Amazon", url="http://amazon.com")
amazon.save()