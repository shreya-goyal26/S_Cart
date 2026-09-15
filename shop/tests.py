from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Product, Order, OrderUpdate, Review, ProductInquiry, ContactMessage
import json

class ShopMarketplaceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.seller = User.objects.create_user(
            username="seller_jane",
            email="jane@store.com",
            password="password123",
            first_name="Jane",
            last_name="Seller"
        )
        self.buyer = User.objects.create_user(
            username="buyer_john",
            email="john@buyer.com",
            password="password123",
            first_name="John",
            last_name="Buyer"
        )
        self.product = Product.objects.create(
            seller=self.seller,
            seller_name="Jane Tech Boutique",
            seller_contact="jane@store.com | +91 98765 00000",
            product_name="Pro Noise Cancelling Earbuds",
            category="Audio",
            subcategory="Earbuds",
            price=4999,
            original_price=6999,
            desc="Top quality wireless earbuds with high definition audio.",
            features="ANC | 30h battery | Wireless charging",
            rating=4.5,
            rating_count=1,
            in_stock=True
        )

    def test_homepage_loads_products(self):
        response = self.client.get(reverse('ShopHome'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pro Noise Cancelling Earbuds")

    def test_search_and_filter(self):
        response = self.client.get(reverse('ShopSearch') + '?q=Earbuds')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pro Noise Cancelling Earbuds")

    def test_product_detail_view(self):
        response = self.client.get(reverse('ShopProductView', args=[self.product.product_id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pro Noise Cancelling Earbuds")
        self.assertContains(response, "Jane Tech Boutique")

    def test_buyer_reach_out_inquiry(self):
        response = self.client.post(reverse('ShopProductInquiry', args=[self.product.product_id]), {
            'name': 'Interested Customer',
            'email': 'customer@test.com',
            'phone': '+91 98888 77777',
            'subject': 'Warranty question',
            'message': 'Do these earbuds come with 1-year replacement warranty?'
        })
        self.assertEqual(ProductInquiry.objects.count(), 1)
        inquiry = ProductInquiry.objects.first()
        self.assertEqual(inquiry.name, 'Interested Customer')
        self.assertEqual(inquiry.product, self.product)

    def test_customer_review_updates_rating(self):
        response = self.client.post(reverse('ShopAddReview', args=[self.product.product_id]), {
            'user_name': 'Happy Audiophile',
            'rating': 5,
            'comment': 'Phenomenal audio clarity and super fast delivery!'
        })
        self.assertEqual(Review.objects.count(), 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.rating, 5.0)
        self.assertEqual(self.product.rating_count, 1)

    def test_seller_adds_product_via_dashboard(self):
        self.client.login(username='seller_jane', password='password123')
        response = self.client.post(reverse('ShopAddProduct'), {
            'product_name': 'Mechanical Gaming Numpad',
            'category': 'Electronics',
            'subcategory': 'Accessories',
            'price': '1999',
            'original_price': '2999',
            'desc': 'Hot-swappable RGB numpad.',
            'features': 'Hot-swap | RGB',
            'seller_contact': 'jane@store.com',
            'in_stock': 'on'
        })
        self.assertEqual(Product.objects.count(), 2)
        new_prod = Product.objects.get(product_name='Mechanical Gaming Numpad')
        self.assertEqual(new_prod.seller, self.seller)

    def test_cart_api_and_checkout_flow(self):
        # Add to cart
        response = self.client.post(
            reverse('ShopApiCartAdd'),
            data=json.dumps({'product_id': self.product.product_id, 'qty': 2}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        # Checkout
        checkout_resp = self.client.post(reverse('ShopCheckout'), {
            'firstName': 'John',
            'lastName': 'Buyer',
            'email': 'john@buyer.com',
            'phone': '+91 99999 88888',
            'address': '123 Tech Park',
            'city': 'Bengaluru',
            'state': 'Karnataka',
            'zip_code': '560001',
            'paymentMethod': 'Cash on Delivery'
        })
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertTrue(order.order_id.startswith('SC-2024-'))
        self.assertEqual(OrderUpdate.objects.filter(order=order).count(), 1)

        # Track order
        track_resp = self.client.post(reverse('ShopTracker'), {
            'orderId': order.order_id
        })
        self.assertEqual(track_resp.status_code, 200)
        self.assertContains(track_resp, order.order_id)
