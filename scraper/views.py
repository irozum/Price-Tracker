# from django.shortcuts import render
from django.views import View, generic
from scraper.models import Link, Price


class Index(generic.ListView):
    model = Link
    template_name = 'scraper/index.html'
    # ordering = ['-date_generated']