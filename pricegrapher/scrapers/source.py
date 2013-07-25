class Source():
    source_title = ''
    """
    Try to create a new product. If it already exists, return its id.
    """
    def create(self, url):
        pass

    """
    Add a new price model to the database with the most recent price for the given source_id
    source_id is like an ASIN for amazon

    return new price model if we were able to create one
    return false if we failed to get a price from the source
    """
    def add_new_price(self, product):
        pass


