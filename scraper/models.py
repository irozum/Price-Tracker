from django.db import models

class Link(models.Model):
    website_name = models.CharField(max_length=40)
    product_name = models.CharField(max_length=40)
    link = models.URLField()

    def __str__(self):
        return f'{self.product_name} on {self.website_name}'

class Price(models.Model):
    link_id = models.ForeignKey(Link, on_delete=models.CASCADE)
    date_generated = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.link_id.product_name} for {self.price}'