from django.shortcuts import render, get_object_or_404
from .cart import Cart
from core.models import Product
from django.http import JsonResponse

# Create your views here.
def cart_summary(request):
	return render(request, "cart_summary.html", {})

def cart_add(request):
    cart = Cart(request)
    
    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        
        print("Received POST data:", request.POST)  # Debugging line

        if product_id:
            try:
                product_id = int(product_id)
                product = get_object_or_404(Product, id=product_id)
                cart.add(product=product)
                cart_quantity = cart.__len__()
                return JsonResponse({'message': 'Product added to cart successfully.', 'qty': cart_quantity})
            
            except (ValueError, Product.DoesNotExist):
                return JsonResponse({'error': 'Invalid product ID or product does not exist.'}, status=400)
        else:
            return JsonResponse({'error': 'Product ID is missing.'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method or action.'}, status=405)

def cart_delete(request):
	pass

def cart_update(request):
	pass