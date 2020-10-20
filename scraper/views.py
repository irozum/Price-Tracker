from django.views import generic, View
from scraper.models import Link, Price, Website
from django.shortcuts import redirect, render
from urllib.parse import urlparse
from .forms import LinkForm
from django.contrib import messages
from django.core.paginator import Paginator


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
        website_id = request.POST.get('website', '')
        website = Website.objects.get(pk=website_id)

        if website.domain not in link:
            messages.error(request, "Selected website and provided url don't match")
            return redirect('/')

        Link(website=website, product_name=product, url=link).save()
        messages.success(request, "Product has been added")
        return redirect('/')


class LinkDelete(generic.DeleteView):
    model = Link
    success_url = '/'


class History(View):
    def get(self, request, *args, **kwargs):
        link = Link.objects.get(pk=self.kwargs['pk'])

        prices = Price.objects.filter(link=self.kwargs['pk']).order_by('-pk')
        paginator = Paginator(prices, 25)

        page_number = request.GET.get('page', 1)

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        context = {
            'prices': page_obj,
            'product_name': link.product_name
        }
        return render(request, 'scraper/price_history.html', context)
