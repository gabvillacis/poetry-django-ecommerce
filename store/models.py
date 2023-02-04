from django.db import models
from django.contrib.auth.models import User

"""Definición de modelo Category para almacenar las categorías de productos"""
class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        db_table = 'st_categories'
        verbose_name_plural = 'categories'        

    def __str__(self) -> str:
        return 'Categoría: ' + self.name
    
    
"""Definición de modelo Product para almacenar el inventario de productos"""
class Product(models.Model):    
    category = models.ManyToManyField(Category, related_name="products")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'st_products'

    def __str__(self) -> str:
        return 'Producto: ' + self.name


"""Definición de modelo Address para almacenar las direcciones de los usuarios"""
class Address(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    cellphone = models.CharField(max_length=13)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'st_addresses'
        verbose_name_plural = 'addresses'

    def __str__(self) -> str:
        return 'Dirección: ' + self.id


"""Definición de modelo Order para almacenar los pedidos generados"""
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)	

    class Meta:
        db_table = 'st_orders'        

    def __str__(self) -> str:
        return 'Pedido: ' + str(self.id)
	
    @property
    def total(self):
        order_items = self.order_items.all()
        total = sum([item.get_subtotal for item in order_items])
        return total

    @property
    def count_items(self):
        order_items = self.order_items.all()
        count = sum([item.quantity for item in order_items])
        return count


"""Definición de modelo OrderItem para almacenar los items de los pedidos"""
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'st_order_items'
        verbose_name_plural = 'order_items'

    def __str__(self) -> str:
        return 'Item: ' + str(self.id)
	
    @property
    def subtotal(self):
        subtotal = self.product.price * self.quantity
        return subtotal