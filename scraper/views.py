from django.views import generic, View
from scraper.models import Link, Price, Website
from django.shortcuts import redirect, render
from urllib.parse import urlparse
from .forms import LinkForm
from django.contrib import messages


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
            messages.error(request, "Website and link don't match")
            return redirect('/')

        Link(website=website, product_name=product, url=link).save()
        messages.success(request, "Product has been added")
        return redirect('/')


class LinkDelete(generic.DeleteView):
    model = Link
    success_url = '/'


class History(generic.ListView):
    model = Price
    template_name = 'scraper/price_history.html'
    ordering = ['-id']
    paginate_by = 50
