from django.contrib import admin
from .models import Product, Order, OrderUpdate, ContactMessage, Review, ProductInquiry

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'seller_name', 'category', 'price', 'original_price', 'rating', 'in_stock', 'is_featured', 'is_deal_of_the_day')
    list_filter = ('category', 'in_stock', 'is_featured', 'is_deal_of_the_day', 'pub_date')
    search_fields = ('product_name', 'desc', 'category', 'seller_name')

@admin.register(ProductInquiry)
class ProductInquiryAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'email', 'phone', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'message', 'product__product_name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'name', 'amount', 'status', 'payment_method', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_method', 'payment_status', 'created_at')
    search_fields = ('order_id', 'name', 'email', 'phone')

@admin.register(OrderUpdate)
class OrderUpdateAdmin(admin.ModelAdmin):
    list_display = ('order', 'update_desc', 'timestamp')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user_name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
