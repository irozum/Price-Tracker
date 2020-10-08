from django.db import models


class Website(models.Model):
    name = models.CharField(max_length=40)
    domain = models.CharField(max_length=60)
    price_getter_type = models.CharField(max_length=50)
    price_getter = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Link(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, default='')
    product_name = models.CharField(max_length=40)
    url = models.URLField()

    def __str__(self):
        return f'{self.product_name} on {self.website.name}'


class Price(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    date_generated = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.link.product_name} for {self.price}'
