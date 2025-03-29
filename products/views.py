from django.shortcuts import render
from django.http import JsonResponse
from .models import Products

def product_list(request):
    products = Products.objects.all()  # Ottieni tutti i prodotti dal database
    return render(request, 'product_list.html', {'products': products})


def products_api(request):
    products = Products.objects.all()
    data = [
        {
            'product_code': p.product_code,
            'name': p.name,
            'price': float(p.price),
        }
        for p in products
    ]
    return JsonResponse(data, safe=False)
