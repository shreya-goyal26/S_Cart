import json
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count, Avg
from .models import Product, Order, OrderUpdate, ContactMessage, Review, ProductInquiry


# ==========================================
# SHOP VIEWS
# ==========================================

def index(request):
    featured_products = Product.objects.filter(is_featured=True).order_by('-pub_date')[:8]
    if not featured_products.exists():
        featured_products = Product.objects.all().order_by('-pub_date')[:8]

    recent_products = Product.objects.all().order_by('-pub_date')[:12]
    categories = Product.objects.values('category').annotate(count=Count('product_id')).order_by('-count')
    deals = Product.objects.filter(is_deal_of_the_day=True)[:4]

    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_sellers = User.objects.filter(products__isnull=False).distinct().count()

    context = {
        'products': recent_products,
        'featured_products': featured_products,
        'categories': categories,
        'deals': deals,
        'stats': {
            'products': total_products,
            'orders': total_orders,
            'sellers': total_sellers,
        }
    }
    return render(request, "shop/index.html", context)


def about(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users,
    }
    return render(request, "shop/about.html", context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        first_name = request.POST.get('firstName', '').strip()
        last_name = request.POST.get('lastName', '').strip()
        if not name and (first_name or last_name):
            name = f"{first_name} {last_name}".strip()

        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        if name and email and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message_text
            )
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                return JsonResponse({'status': 'success', 'message': 'Thank you! Your message has been sent.'})
            messages.success(request, "Thank you! Your message has been received. Our team will contact you shortly.")
            return redirect('ShopContact')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Please fill out all required fields.'}, status=400)
            messages.error(request, "Please fill out all required fields.")

    return render(request, "shop/contact.html")


def search(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    sort = request.GET.get('sort', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    in_stock_only = request.GET.get('in_stock', '').strip()

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(product_name__icontains=query) |
            Q(desc__icontains=query) |
            Q(category__icontains=query) |
            Q(subcategory__icontains=query) |
            Q(seller_name__icontains=query)
        )
    if category and category.lower() != 'all':
        products = products.filter(category__iexact=category)

    if min_price and min_price.isdigit():
        products = products.filter(price__gte=int(min_price))
    if max_price and max_price.isdigit():
        products = products.filter(price__lte=int(max_price))

    if in_stock_only == '1':
        products = products.filter(in_stock=True)

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating')
    elif sort == 'newest':
        products = products.order_by('-pub_date')
    else:
        products = products.order_by('-pub_date')

    all_categories = Product.objects.values('category').annotate(count=Count('product_id')).order_by('-count')

    context = {
        'products': products,
        'query': query,
        'category': category,
        'sort': sort,
        'min_price': min_price,
        'max_price': max_price,
        'all_categories': all_categories,
        'result_count': products.count(),
    }
    return render(request, "shop/search.html", context)


def productView(request, myid):
    product = get_object_or_404(Product, product_id=myid)
    reviews = product.reviews.all().order_by('-created_at')
    related = Product.objects.filter(category=product.category).exclude(product_id=myid)[:4]

    context = {
        'product': product,
        'reviews': reviews,
        'review_count': reviews.count(),
        'related_products': related,
    }
    return render(request, "shop/productView.html", context)


def product_inquiry(request, myid):
    """Allows buyers to reach out to the seller of a product directly."""
    product = get_object_or_404(Product, product_id=myid)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', f"Inquiry about {product.product_name}").strip()
        message_text = request.POST.get('message', '').strip()

        if name and email and message_text:
            sender = request.user if request.user.is_authenticated else None
            inquiry = ProductInquiry.objects.create(
                product=product,
                sender=sender,
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message_text
            )
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': f"Your inquiry has been sent to {product.seller_name or 'the seller'}! They will reach out to you via {email}."
                })
            messages.success(request, f"Your inquiry has been sent to {product.seller_name or 'the seller'}! They will reach out to you at {email}.")
            return redirect('ShopProductView', myid=product.product_id)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Please fill all required fields.'}, status=400)
            messages.error(request, "Please provide your name, email, and message.")

    return redirect('ShopProductView', myid=product.product_id)


def add_review(request, myid):
    """Allows users to submit a review for a product."""
    product = get_object_or_404(Product, product_id=myid)

    if request.method == 'POST':
        user_name = request.POST.get('user_name', '').strip()
        if request.user.is_authenticated and not user_name:
            user_name = request.user.get_full_name() or request.user.username
        if not user_name:
            user_name = "Anonymous Buyer"

        try:
            rating = int(request.POST.get('rating', 5))
            rating = max(1, min(5, rating))
        except (ValueError, TypeError):
            rating = 5

        comment = request.POST.get('comment', '').strip()
        if comment:
            user = request.user if request.user.is_authenticated else None
            Review.objects.create(
                product=product,
                user=user,
                user_name=user_name,
                rating=rating,
                comment=comment
            )
            product.update_rating()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Review submitted successfully! Thank you for your feedback.',
                    'new_rating': product.rating,
                    'rating_count': product.rating_count
                })
            messages.success(request, "Your review has been submitted successfully!")
            return redirect('ShopProductView', myid=product.product_id)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Please write a comment for your review.'}, status=400)
            messages.error(request, "Please provide a review comment.")

    return redirect('ShopProductView', myid=product.product_id)


# ==========================================
# CART & CHECKOUT
# ==========================================

def get_cart_data(session):
    """Helper to build cart items list from session cart dictionary {product_id: qty}"""
    cart = session.get('cart', {})
    cart_items = []
    subtotal = 0

    product_ids = [int(pid) for pid in cart.keys() if str(pid).isdigit() and int(cart[pid]) > 0]
    if product_ids:
        products = Product.objects.filter(product_id__in=product_ids)
        product_map = {p.product_id: p for p in products}

        for pid_str, qty in cart.items():
            if not str(pid_str).isdigit():
                continue
            pid = int(pid_str)
            if pid in product_map and int(qty) > 0:
                p = product_map[pid]
                item_total = p.price * int(qty)
                subtotal += item_total
                cart_items.append({
                    'product_id': p.product_id,
                    'name': p.product_name,
                    'price': p.price,
                    'original_price': p.original_price,
                    'qty': int(qty),
                    'total': item_total,
                    'image': p.display_image,
                    'category': p.category,
                })

    tax = int(subtotal * 0.18)  # 18% GST standard
    total = subtotal + tax

    return {
        'items': cart_items,
        'count': sum(item['qty'] for item in cart_items),
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
    }


def api_get_cart(request):
    data = get_cart_data(request.session)
    return JsonResponse(data)


@require_POST
def api_add_to_cart(request):
    try:
        data = json.loads(request.body) if request.body else request.POST
        product_id = str(data.get('product_id', ''))
        qty = int(data.get('qty', 1))

        if not product_id or not Product.objects.filter(product_id=product_id).exists():
            return JsonResponse({'status': 'error', 'message': 'Invalid product'}, status=400)

        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + max(1, qty)
        request.session['cart'] = cart
        request.session.modified = True

        cart_data = get_cart_data(request.session)
        return JsonResponse({
            'status': 'success',
            'message': 'Product added to cart!',
            'cart': cart_data
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@require_POST
def api_update_cart(request):
    try:
        data = json.loads(request.body) if request.body else request.POST
        product_id = str(data.get('product_id', ''))
        action = data.get('action', 'update')  # 'update', 'remove'
        qty = int(data.get('qty', 0))

        cart = request.session.get('cart', {})
        if product_id in cart:
            if action == 'remove' or qty <= 0:
                del cart[product_id]
            else:
                cart[product_id] = qty

        request.session['cart'] = cart
        request.session.modified = True

        cart_data = get_cart_data(request.session)
        return JsonResponse({
            'status': 'success',
            'cart': cart_data
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@require_POST
def api_clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    return JsonResponse({'status': 'success', 'cart': get_cart_data(request.session)})


def checkout(request):
    cart_data = get_cart_data(request.session)

    if request.method == 'POST':
        # Handle order placement
        first_name = request.POST.get('firstName', '').strip()
        last_name = request.POST.get('lastName', '').strip()
        name = f"{first_name} {last_name}".strip() or request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        zip_code = request.POST.get('zip_code', '').strip() or request.POST.get('pin', '').strip()
        payment_method = request.POST.get('paymentMethod', 'Cash on Delivery')

        # Use items from POST or session cart
        items_json_str = request.POST.get('items_json', '')
        if not items_json_str and cart_data['items']:
            items_json_str = json.dumps(cart_data['items'])

        amount_str = request.POST.get('amount', '')
        try:
            amount = int(float(amount_str)) if amount_str else cart_data['total']
        except (ValueError, TypeError):
            amount = cart_data['total']

        if not name or not email or not phone or not address or not city or not zip_code:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Please fill out all required shipping fields.'}, status=400)
            messages.error(request, "Please fill out all required shipping fields.")
            return render(request, "shop/checkout.html", {'cart': cart_data})

        # Generate unique order ID: SC-2024-XXXXX
        rand_num = random.randint(10000, 99999)
        order_id = f"SC-2024-{rand_num}"
        while Order.objects.filter(order_id=order_id).exists():
            rand_num = random.randint(10000, 99999)
            order_id = f"SC-2024-{rand_num}"

        user = request.user if request.user.is_authenticated else None

        order = Order.objects.create(
            order_id=order_id,
            user=user,
            name=name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            items_json=items_json_str or "[]",
            amount=amount,
            status="Order Placed",
            payment_method=payment_method,
            payment_status="Completed" if payment_method != "Cash on Delivery" else "Pending",
            courier="BlueDart Express",
            tracking_number=f"BD{random.randint(1000000000, 9999999999)}"
        )

        # Create initial order update log
        OrderUpdate.objects.create(
            order=order,
            update_desc=f"Order placed successfully. Payment method: {payment_method}."
        )

        # Clear session cart
        request.session['cart'] = {}
        request.session.modified = True

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax') == '1':
            return JsonResponse({
                'status': 'success',
                'order_id': order.order_id,
                'redirect_url': f"/shop/order-success/{order.order_id}/"
            })

        return redirect('ShopOrderSuccess', order_id=order.order_id)

    context = {
        'cart': cart_data,
    }
    return render(request, "shop/checkout.html", context)


def order_success(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    items = order.get_items()
    updates = order.updates.all().order_by('-timestamp')
    context = {
        'order': order,
        'items': items,
        'updates': updates,
    }
    return render(request, "shop/order_success.html", context)


# ==========================================
# TRACKER
# ==========================================

def tracker(request):
    if request.method == 'POST':
        order_id = request.POST.get('orderId', '').strip()
        email = request.POST.get('trackEmail', '').strip()

        orders = Order.objects.none()
        if order_id:
            orders = Order.objects.filter(order_id__iexact=order_id)
        elif email:
            orders = Order.objects.filter(email__iexact=email).order_by('-created_at')

        if orders.exists():
            order = orders.first()
            updates = order.updates.all().order_by('-timestamp')
            items = order.get_items()

            status_progress = {
                'Order Placed': 25,
                'Dispatched': 50,
                'In Transit': 75,
                'Out for Delivery': 90,
                'Delivered': 100,
                'Cancelled': 0,
            }
            progress = status_progress.get(order.status, 25)

            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax') == '1':
                updates_data = [{'desc': u.update_desc, 'time': u.timestamp.strftime('%b %d, %Y - %I:%M %p')} for u in updates]
                return JsonResponse({
                    'status': 'success',
                    'order': {
                        'order_id': order.order_id,
                        'name': order.name,
                        'status': order.status,
                        'amount': order.amount,
                        'courier': order.courier,
                        'tracking_number': order.tracking_number,
                        'progress': progress,
                        'created_at': order.created_at.strftime('%b %d, %Y'),
                        'address': f"{order.address}, {order.city}, {order.state} - {order.zip_code}",
                        'items': items,
                    },
                    'updates': updates_data
                })

            context = {
                'order': order,
                'updates': updates,
                'items': items,
                'progress': progress,
                'found': True,
            }
            return render(request, "shop/tracker.html", context)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax') == '1':
                return JsonResponse({'status': 'error', 'message': 'No matching order found with the provided details.'}, status=404)
            messages.error(request, "No order found matching your Order ID or Email.")
            return render(request, "shop/tracker.html", {'found': False})

    # GET request: check query params if direct link
    order_id = request.GET.get('order_id', '').strip()
    if order_id:
        try:
            order = Order.objects.get(order_id__iexact=order_id)
            updates = order.updates.all().order_by('-timestamp')
            items = order.get_items()
            status_progress = {
                'Order Placed': 25,
                'Dispatched': 50,
                'In Transit': 75,
                'Out for Delivery': 90,
                'Delivered': 100,
                'Cancelled': 0,
            }
            return render(request, "shop/tracker.html", {
                'order': order,
                'updates': updates,
                'items': items,
                'progress': status_progress.get(order.status, 25),
                'found': True,
            })
        except Order.DoesNotExist:
            pass

    return render(request, "shop/tracker.html", {'found': False})


# ==========================================
# USER AUTHENTICATION & SELLER DASHBOARD
# ==========================================

def register_view(request):
    if request.user.is_authenticated:
        return redirect('ShopDashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        if not username or not email or not password:
            messages.error(request, "Please fill in all required fields.")
            return render(request, "shop/auth.html", {'active_tab': 'register'})

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "shop/auth.html", {'active_tab': 'register'})

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken. Please choose another.")
            return render(request, "shop/auth.html", {'active_tab': 'register'})

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, "shop/auth.html", {'active_tab': 'register'})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        login(request, user)
        messages.success(request, f"Welcome to S_Cart, {user.first_name or user.username}! Your account has been created.")
        return redirect('ShopDashboard')

    return render(request, "shop/auth.html", {'active_tab': 'register'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('ShopDashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is None:
            # Also allow login with email
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next') or request.POST.get('next') or 'ShopDashboard'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "shop/auth.html", {'active_tab': 'login'})

    return render(request, "shop/auth.html", {'active_tab': 'login'})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('ShopHome')


@login_required(login_url='ShopLogin')
def dashboard_view(request):
    """User & Seller Portal: Manage listed products, view customer inquiries, my orders, blog posts."""
    my_products = Product.objects.filter(seller=request.user).order_by('-pub_date')
    my_orders = Order.objects.filter(Q(user=request.user) | Q(email=request.user.email)).order_by('-created_at')

    # Inquiries received for products listed by this user
    received_inquiries = ProductInquiry.objects.filter(product__seller=request.user).order_by('-created_at')
    # Inquiries sent by this user
    sent_inquiries = ProductInquiry.objects.filter(sender=request.user).order_by('-created_at')

    # Blog posts written by this user
    from blog.models import BlogPost
    my_articles = BlogPost.objects.filter(author_user=request.user).order_by('-pub_date')

    all_categories = Product.objects.values_list('category', flat=True).distinct()

    context = {
        'my_products': my_products,
        'my_orders': my_orders,
        'received_inquiries': received_inquiries,
        'unread_inquiries_count': received_inquiries.filter(is_read=False).count(),
        'sent_inquiries': sent_inquiries,
        'my_articles': my_articles,
        'categories': all_categories,
    }
    return render(request, "shop/dashboard.html", context)


@login_required(login_url='ShopLogin')
def add_product_view(request):
    """Allows any logged in user/seller to list their product in the real database."""
    if request.method == 'POST':
        product_name = request.POST.get('product_name', '').strip()
        category = request.POST.get('category', '').strip()
        subcategory = request.POST.get('subcategory', '').strip()
        price_str = request.POST.get('price', '0').strip()
        original_price_str = request.POST.get('original_price', '0').strip()
        desc = request.POST.get('desc', '').strip()
        features = request.POST.get('features', '').strip()
        seller_contact = request.POST.get('seller_contact', '').strip()
        image_url = request.POST.get('image_url', '').strip()
        in_stock = request.POST.get('in_stock') == 'on' or request.POST.get('in_stock') == 'true'

        if not product_name or not category or not price_str or not desc:
            messages.error(request, "Please fill in all required fields (Name, Category, Price, and Description).")
            return redirect('ShopDashboard')

        try:
            price = int(float(price_str))
            original_price = int(float(original_price_str)) if original_price_str else price
        except ValueError:
            price = 0
            original_price = 0

        seller_name = request.user.get_full_name() or request.user.username
        if not seller_contact:
            seller_contact = request.user.email

        product = Product(
            seller=request.user,
            seller_name=seller_name,
            seller_contact=seller_contact,
            product_name=product_name,
            category=category,
            subcategory=subcategory,
            price=price,
            original_price=original_price,
            desc=desc,
            features=features,
            image_url=image_url,
            in_stock=in_stock,
            rating=5.0,
            rating_count=0
        )

        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()
        messages.success(request, f"🎉 '{product.product_name}' has been successfully listed in the store! Users can now find and buy or reach out to you.")
        return redirect('ShopDashboard')

    return redirect('ShopDashboard')


@login_required(login_url='ShopLogin')
def edit_product_view(request, myid):
    product = get_object_or_404(Product, product_id=myid)
    if product.seller != request.user and not request.user.is_staff:
        messages.error(request, "You do not have permission to edit this product.")
        return redirect('ShopDashboard')

    if request.method == 'POST':
        product.product_name = request.POST.get('product_name', product.product_name).strip()
        product.category = request.POST.get('category', product.category).strip()
        product.subcategory = request.POST.get('subcategory', product.subcategory).strip()

        try:
            product.price = int(float(request.POST.get('price', product.price)))
            product.original_price = int(float(request.POST.get('original_price', product.original_price)))
        except ValueError:
            pass

        product.desc = request.POST.get('desc', product.desc).strip()
        product.features = request.POST.get('features', product.features).strip()
        product.seller_contact = request.POST.get('seller_contact', product.seller_contact).strip()
        product.image_url = request.POST.get('image_url', product.image_url).strip()
        product.in_stock = request.POST.get('in_stock') == 'on' or request.POST.get('in_stock') == 'true'

        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()
        messages.success(request, f"Product '{product.product_name}' updated successfully!")
        return redirect('ShopDashboard')

    all_categories = Product.objects.values_list('category', flat=True).distinct()
    return render(request, "shop/edit_product.html", {'product': product, 'categories': all_categories})


@login_required(login_url='ShopLogin')
def delete_product_view(request, myid):
    product = get_object_or_404(Product, product_id=myid)
    if product.seller != request.user and not request.user.is_staff:
        messages.error(request, "You do not have permission to delete this product.")
        return redirect('ShopDashboard')

    product_name = product.product_name
    product.delete()
    messages.success(request, f"Product '{product_name}' has been deleted.")
    return redirect('ShopDashboard')


@login_required(login_url='ShopLogin')
def mark_inquiry_read(request, inquiry_id):
    inquiry = get_object_or_404(ProductInquiry, inquiry_id=inquiry_id)
    if inquiry.product.seller == request.user or request.user.is_staff:
        inquiry.is_read = True
        inquiry.save(update_fields=['is_read'])
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)


# Fallback stubs for existing urls
def handlerequest(request):
    return redirect('ShopHome')

def paymenthandler(request):
    return redirect('ShopHome')