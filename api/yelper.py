#Attempting yelp scraping

from yelp.client import Client

MY_API_KEY = '0X8SzKkV2v7bo9s_vUvl7IR23KFICRqBaucXJ9DOYQlhgDqXgOeZuzk3ruirXyphW0O6cZXrQfzJRgaHREFQNiBIDXzmwDUvgWdNBQRGLezZ4h7a1D4G8H8Wi-e3W3Yx'

client = Client(MY_API_KEY)

business_response = client.business.get_by_id('yelp-reno')

print(business_response)