from scraper.models import Link, Price
from bs4 import BeautifulSoup
import os
import smtplib
from email.message import EmailMessage
import requests
import time
import datetime


HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


def sendEmail(difference, product, url, old_price, new_price):
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

    msg = EmailMessage()
    msg['Subject'] = f'Price has {difference} for {product}'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'farkop69@gmail.com'
    content = f'''Price has {difference} for {product}: {old_price} -> {new_price}.
                   
    Link: {url}'''
    msg.set_content(content)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


def check():
    links = Link.objects.all()
    list_length = len(links)

    for n, link in enumerate(links):

        # Skip if price was saved today already
        last_price = Price.objects.filter(link=link).order_by('-id')[0]
        if last_price is not None:
            last_saved_day = last_price.date_generated.strftime('%d')
            today_day = datetime.datetime.today().strftime('%d')
            if today_day == last_saved_day:
                break

        # Get page content
        page = requests.get(link.url, headers=HEADERS)
        soup = BeautifulSoup(page.content, 'html.parser')
        price_element = soup.find(id='priceblock_ourprice')
        
        # If no response from website, print it's content 
        if price_element is None:
            print(soup)
            continue
        
        # Get and save new price
        newPrice = soup.find(id='priceblock_ourprice').get_text()
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


if '__name__' == '__main__':
    check()