from .models import Product

CART_SESSION_ID = 'cart'

class ShoppingCartSession:

    """Inicializando el shopping cart"""
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    """Agregar item al cart"""
    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        
        if product_id not in self.cart:
            self.cart[product_id] = quantity
        else:
            self.cart[product_id] += quantity
        
        self.save()


    """Actualizar cantidad de item en el cart"""
    def update(self, product_id, quantity):
        product_id = str(product_id)

        if product_id in self.cart:
            self.cart[product_id] = quantity
        
        self.save()


    """Quitar item del cart"""
    def delete(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]            

        self.save()


    def save(self):
        self.session.modified = True
        

    def clear(self):
        del self.session[CART_SESSION_ID]


    """Contabilizar todas las unidades agregadas al carrito"""
    def __len__(self):
        return sum(self.cart.values())
    
    """Obtener el detalle de los productos que están en el carrito"""
    def get_cart_detail(self):
        cart_items = []
                
        for product_id, quantity in self.cart.items():
            product = Product.objects.get(pk=product_id)
            cart_items.append({'product': product,
                               'quantity': quantity,
                               'subtotal': product.price * quantity})
        return cart_items
    
    
    """Obtener el monto total de los items del carrito"""
    def get_total(self):        
        return sum(item['subtotal'] for item in self.get_cart_detail())