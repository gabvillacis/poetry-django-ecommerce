from django.contrib import admin
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','slug')
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('name','slug', 'description', 'price', 'is_active')
    list_filter=('categories',)
    search_fields=("name__startswith",)

class ItemInline(admin.TabularInline):    
    fields = ('id', 'product', 'quantity')
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('id', 'user', 'address', 'total_amount', 'created_at')
    inlines = (ItemInline,)