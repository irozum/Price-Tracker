from django.core.management.base import BaseCommand
from scraper.utils import price_tracker

class Command(BaseCommand):
    def handle(self, **options):
        price_tracker.check()
