from urllib.parse import quote_plus
def platform_url(p,q):
    q=quote_plus(q); m={'Amazon':f'https://www.amazon.in/s?k={q}','Flipkart':f'https://www.flipkart.com/search?q={q}','IKEA':f'https://www.ikea.com/in/en/search/?q={q}','Swiggy':f'https://www.swiggy.com/search?query={q}','Zomato':f'https://www.zomato.com/search?q={q}','OYO':f'https://www.oyorooms.com/search?location={q}'}
    return m.get(p,f'https://www.google.com/search?q={q}')
