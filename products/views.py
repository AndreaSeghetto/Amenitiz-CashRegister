from django.shortcuts import render
from .models import Products

def product_list(request):
    products = Products.objects.all()  # Ottieni tutti i prodotti dal database
    return render(request, 'product_list.html', {'products': products})
