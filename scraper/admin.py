from django.contrib import admin
from .models import Link, Price, Website

admin.site.register(Website)
admin.site.register(Link)
admin.site.register(Price)
