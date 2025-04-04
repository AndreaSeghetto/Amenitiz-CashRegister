from django.db import models

class Products(models.Model):
    product_code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name