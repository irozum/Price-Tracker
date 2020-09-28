from django.views import generic
from scraper.models import Link, Price
from django.shortcuts import redirect
from urllib.parse import urlparse


class Index(generic.ListView):
    model = Link
    template_name = 'scraper/index.html'

    def post(self, request, *args, **kwargs):
        product = request.POST.get('product', '')
        link = request.POST.get('link', '')
        domain = urlparse(link).netloc
        website = domain if domain else 'N/A'
        Link(website_name=website, product_name=product, link=link).save()
        return redirect('/')
