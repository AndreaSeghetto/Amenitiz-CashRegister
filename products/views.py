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
    Returns a JSON response with the total price and a summary of items.

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
            # Iterate over each unique product code and its corresponding quantity
            for code, quantity in counts.items():
                try:
                    # Retrieve the product details from the database
                    product = Products.objects.get(product_code=code)
                    # Append the product name and quantity to the summary list
                    summary.append({
                        "product_code": product.product_code,
                        "name": product.name,
                        "quantity": quantity
                    })
                except Products.DoesNotExist:
                    # If a product code does not exist in the database, skip it
                    continue

            # Construct the response data with the total price and item summary
            response_data = {
                "total": total,
                "summary": summary
            }
            return JsonResponse(response_data)

        except Exception as e:
            # Return an error response if any exception occurs during processing
            return JsonResponse({"error": str(e)}, status=400)
    else:
        # Return an error response if the request method is not POST
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

