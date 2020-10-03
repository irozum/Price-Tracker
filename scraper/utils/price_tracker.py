from scraper.models import Link, Price

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


import os
import smtplib
from email.message import EmailMessage


# HEADERS = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
# }


def sendEmail(difference, product, url, old_price, new_price):
    EMAIL_ADDRESS = 'farkop69f@gmail.com'
    EMAIL_PASSWORD = 'gazpachoRVD4112'

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
    driver_location = '/Users/irozum/Dev/Python/Scraper/scraper_project/scraper/utils/chromedriver'
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    executable_path = os.environ.get("CHROMEDRIVER_PATH") if os.environ.get("CHROMEDRIVER_PATH") else driver_location
    driver = webdriver.Chrome(executable_path=executable_path, options=options)


    links = Link.objects.all()
    for link in links:
    #     page = requests.get(link.url, headers=HEADERS)
    #     soup = BeautifulSoup(page.content, 'html.parser')

    #     print(soup)



        driver.get(link.url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        print(soup)

        newPrice = soup.find(id='priceblock_ourprice').get_text().strip()
        i = [x.isdigit() for x in newPrice].index(True)
        newPrice = round(float(newPrice[i:]), 2)

        print(newPrice)

        newPrice = Price(link=link, price=newPrice)
        newPrice.save()

        prices = Price.objects.filter(link=link).order_by('-id')
        if len(prices) == 1: break
        todayPrice = prices[0].price
        yesterdayPrice = prices[1].price

        if (todayPrice != yesterdayPrice):
            difference = 'increased' if todayPrice > yesterdayPrice else 'decreased'
            # sendEmail(difference, link.product_name, link.url, yesterdayPrice, todayPrice)

    driver.quit()


if '__name__' == '__main__':
    check()