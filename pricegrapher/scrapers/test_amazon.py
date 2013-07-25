import urllib2
from bs4 import BeautifulSoup as bs
def scrape_product(asin):
    url = 'http://www.amazon.com/gp/product/' + asin
    html = urllib2.urlopen(url).read()
    soup = bs(html)
    title = soup.find('span', id='btAsinTitle')
    title_string = title.text
    print title_string

    price_string = soup.find('b', attrs={'class':'priceLarge'}).text
    price_amount = int(float(price_string.replace('$', '')) * 100)
    print price_amount

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
    print description
scrape_product('B004JMZGM2')