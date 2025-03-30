from django.shortcuts import render
from django.http import JsonResponse
from .models import Products
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import calculate_total
from collections import Counter

def product_list(request):
    # Renders the product list as an HTML page (for the template-based version)
    products = Products.objects.all()
    return render(request, 'product_list.html', {'products': products})

def products_api(request):
    # Returns all products as JSON (used by React frontend)
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

@csrf_exempt  # Temporarily exempt this view from CSRF verification for development purposes
def checkout_view(request):
    """
    Handles the checkout process by calculating the total price and summarizing the items.

    Accepts a POST request containing a JSON payload with a list of product codes.
    Returns a JSON response with the total price, a summary of items, and total savings.
    """
    if request.method == "POST":
        try:
            # Parse the JSON payload from the request body
            data = json.loads(request.body)
            # Retrieve the list of product codes; default to an empty list if not provided
            product_codes = data.get("items", [])

            # Calculate the total price using the provided product codes
            total = calculate_total(product_codes)

            # Count the occurrences of each product code to determine quantities
            counts = Counter(product_codes)

            summary = []
            total_savings = 0

            # Iterate over each unique product code and its corresponding quantity
            for code, quantity in counts.items():
                try:
                    # Retrieve the product details from the database
                    product = Products.objects.get(product_code=code)

                    # Determine unit price and full (non-discounted) price
                    unit_price = float(product.price)
                    full_price = unit_price * quantity

                    # Calculate discounted subtotal using calculate_total
                    subtotal = float(calculate_total([code] * quantity))

                    # Calculate savings and accumulate total savings
                    savings = round(full_price - subtotal, 2)
                    total_savings += savings if savings > 0 else 0

                    # Append the product summary with discount information if applicable
                    summary.append({
                        "product_code": product.product_code,
                        "name": product.name,
                        "quantity": quantity,
                        "unit_price": round(unit_price, 2),
                        "full_price": round(full_price, 2),
                        "subtotal": round(subtotal, 2),
                        "savings": savings if savings > 0 else 0
                    })

                except Products.DoesNotExist:
                    # If a product code does not exist in the database, skip it
                    continue

            # Construct the response data with the total price, item summary, and total savings
            response_data = {
                "total": total,
                "total_savings": round(total_savings, 2),
                "summary": summary
            }
            return JsonResponse(response_data)

        except Exception as e:
            # Return an error response if any exception occurs during processing
            return JsonResponse({"error": str(e)}, status=400)
    else:
        # Return an error response if the request method is not POST
        return JsonResponse({"error": "Only POST method allowed"}, status=405)


