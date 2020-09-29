from django.views import generic, View
from scraper.models import Link, Price
from django.shortcuts import redirect, render
from urllib.parse import urlparse
from .forms import LinkForm

from django.http import HttpResponse


class Index(View):
    def get(self, request):
        links = Link.objects.all()
        context = {
            'links': links,
            'form': LinkForm
        }        
        return render(request, 'scraper/index.html', context)

    def post(self, request):
        product = request.POST.get('product', '')
        link = request.POST.get('link', '')
        domain = urlparse(link).netloc
        website = domain if domain else 'N/A'
        Link(website_name=website, product_name=product, link=link).save()
        return redirect('/')

    def delete(self, request):
        return HttpResponse('deleted')
