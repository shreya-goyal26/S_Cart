from django.db import models
from django.contrib.auth.models import User
import json

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    seller_name = models.CharField(max_length=100, default="S_Cart Official", blank=True)
    seller_contact = models.CharField(max_length=150, default="", blank=True, help_text="Email or Phone to reach seller")
    product_name = models.CharField(max_length=150)
    category = models.CharField(max_length=100, default="")
    subcategory = models.CharField(max_length=100, default="", blank=True)
    price = models.IntegerField(default=0)  # Selling price in INR
    original_price = models.IntegerField(default=0, blank=True)  # MRP in INR
    desc = models.TextField(default="")
    features = models.TextField(default="", blank=True, help_text="Pipe-separated or newline-separated list of specifications")
    pub_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to="shop/images", default="", blank=True)
    image_url = models.CharField(max_length=500, default="", blank=True)
    rating = models.FloatField(default=4.5)
    rating_count = models.IntegerField(default=0)
    in_stock = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_deal_of_the_day = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name

    @property
    def display_image(self):
        if self.image:
            try:
                return self.image.url
            except Exception:
                pass
        if self.image_url:
            return self.image_url
        return ""

    @property
    def discount_percent(self):
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    @property
    def savings(self):
        if self.original_price and self.original_price > self.price:
            return self.original_price - self.price
        return 0

    @property
    def get_features_list(self):
        if not self.features:
            return []
        if "|" in self.features:
            return [f.strip() for f in self.features.split("|") if f.strip()]
        return [f.strip() for f in self.features.split("\n") if f.strip()]

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            avg = sum(r.rating for r in reviews) / reviews.count()
            self.rating = round(avg, 1)
            self.rating_count = reviews.count()
            self.save(update_fields=['rating', 'rating_count'])


class ProductInquiry(models.Model):
    inquiry_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inquiries')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_inquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length=20, default='', blank=True)
    subject = models.CharField(max_length=200, default='Product Inquiry', blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Inquiry for {self.product.product_name} from {self.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Order Placed', 'Order Placed'),
        ('Dispatched', 'Dispatched'),
        ('In Transit', 'In Transit'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    order_id = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    items_json = models.TextField(help_text="JSON encoded list of ordered items")
    amount = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Order Placed')
    payment_method = models.CharField(max_length=50, default='Cash on Delivery')
    payment_status = models.CharField(max_length=50, default='Pending')
    tracking_number = models.CharField(max_length=100, default='', blank=True)
    courier = models.CharField(max_length=100, default='BlueDart Express')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order_id} by {self.name}"

    def get_items(self):
        try:
            return json.loads(self.items_json)
        except Exception:
            return []


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='updates')
    update_desc = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Update for {self.order.order_id}: {self.update_desc[:40]}"


class ContactMessage(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length=20, default='', blank=True)
    subject = models.CharField(max_length=200, default='')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    user_name = models.CharField(max_length=100)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user_name} for {self.product.product_name}"