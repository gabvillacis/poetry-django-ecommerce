from .models import Category
from .cart_session import ShoppingCartSession

def get_all_categories(request):
    categories = Category.objects.all()
    return {'categories': categories}

def get_shopping_cart_items(request):
    cart = ShoppingCartSession(request)
    cart_items = cart.__len__()
    return {'cart_items': cart_items}