from django.db import models

class Link(models.Model):
    website_name = models.CharField(max_length=40)
    product_name = models.CharField(max_length=40)
    url = models.URLField()

    def __str__(self):
        return f'{self.product_name} on {self.website_name}'

class Price(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    date_generated = models.DateTimeField(auto_now=True)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.link.product_name} for {self.price}'