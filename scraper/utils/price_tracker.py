from scraper.models import Link, Price
from bs4 import BeautifulSoup
import os
import requests
import time
import datetime
from django.core.mail import send_mail
from django.conf import settings


HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


def sendEmail(difference, product, url, old_price, new_price):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['farkop69f@gmail.com']
    subject = f'Price has {difference} for {product}'
    message = f'''Price has {difference} for {product}: {old_price} -> {new_price}.
                
    Link: {url}'''

    try:
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        print(f'Email sending failed: {e}')
    


def get_price(soup, getter_type, getter):
    if getter_type == 'id':
        return soup.find(id=getter)
    elif getter_type == 'class':
        return soup.find_all(class_=getter)[0]
    else:
        return None


def check():
    links = Link.objects.all()
    list_length = len(links)

    for n, link in enumerate(links):
        # Get page content
        counter = 0
        while True:
            page = requests.get(link.url, headers=HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            price = get_price(soup, link.website.price_getter_type, link.website.price_getter)

            if price or counter > 10:
                break
            else:
                counter += 1

        # If no response from website, print it's content
        if price is None:
            print(f'{link.product_name} price could not be fetched')
            continue


        # Get and save new price
        newPrice = price.get_text()
        i = [x.isdigit() for x in newPrice].index(True)
        newPrice = round(float(newPrice[i:]), 2)
        print(newPrice)
        newPrice = Price(link=link, price=newPrice)
        newPrice.save()

        # Compare last 2 prices
        prices = Price.objects.filter(link=link).order_by('-id')
        if len(prices) == 1: break
        todayPrice = prices[0].price
        yesterdayPrice = prices[1].price
        if (todayPrice != yesterdayPrice):
            difference = 'increased' if todayPrice > yesterdayPrice else 'decreased'
            sendEmail(difference, link.product_name, link.url, yesterdayPrice, todayPrice)
        
        # Wait for 1 minute
        if n+1 != list_length:
            for x in range(60):
                print('.', end='', flush=True)
                time.sleep(1)
            print()


if __name__ == '__main__':
    check()