from core.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get the current session cart if it exists, otherwise create a new one
        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        # Make sure cart is available on all site
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {'quantity': quantity, 'price': str(product.price)}
        self.session.modified = True

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_prods(self):
        # Get ids from cart
        product_ids = self.cart.keys()
        # Use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)
        # Return those look up products
        return products
    
    def get_quants(self):
        quantities = {product_id: item['quantity'] for product_id, item in self.cart.items()}
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product.id)
        # Update cart(Dictionnary)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.session.modified = True
        return self.cart
