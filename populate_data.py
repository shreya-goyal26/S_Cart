import os
import django
import random
from datetime import date, datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'S_Cart.settings')
django.setup()

from django.contrib.auth.models import User
from shop.models import Product, Order, OrderUpdate, ContactMessage, Review, ProductInquiry
from blog.models import BlogPost, BlogComment

def seed():
    print("🌱 Seeding database with realistic e-commerce and blog data...")

    # 1. Create Users
    admin_user, _ = User.objects.get_or_create(
        username="admin",
        defaults={"email": "admin@scart.in", "first_name": "Admin", "last_name": "S_Cart", "is_staff": True, "is_superuser": True}
    )
    admin_user.set_password("admin123")
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()

    seller1, _ = User.objects.get_or_create(
        username="arjun_tech",
        defaults={"email": "arjun@apextech.com", "first_name": "Arjun", "last_name": "Sharma"}
    )
    seller1.set_password("seller123")
    seller1.save()

    seller2, _ = User.objects.get_or_create(
        username="sneha_fashion",
        defaults={"email": "sneha@aurafashion.in", "first_name": "Sneha", "last_name": "Patel"}
    )
    seller2.set_password("seller123")
    seller2.save()

    seller3, _ = User.objects.get_or_create(
        username="vikram_lifestyle",
        defaults={"email": "vikram@urbanliving.in", "first_name": "Vikram", "last_name": "Nair"}
    )
    seller3.set_password("seller123")
    seller3.save()

    buyer1, _ = User.objects.get_or_create(
        username="rohit_kumar",
        defaults={"email": "rohit.k@gmail.com", "first_name": "Rohit", "last_name": "Kumar"}
    )
    buyer1.set_password("buyer123")
    buyer1.save()

    print("✅ Users created: admin (admin123), arjun_tech (seller123), sneha_fashion (seller123), vikram_lifestyle (seller123), rohit_kumar (buyer123)")

    # 2. Create Products
    products_data = [
        {
            "seller": seller1,
            "seller_name": "Apex Electronics Hub",
            "seller_contact": "arjun@apextech.com | +91 98765 11223",
            "product_name": "Apex Pro Ultra Smartwatch (OLED Titanium)",
            "category": "Electronics",
            "subcategory": "Wearables",
            "price": 14999,
            "original_price": 19999,
            "desc": "The Apex Pro Ultra features a sapphire glass OLED display, aerospace-grade titanium frame, dual-frequency GPS, 7-day battery life, and comprehensive biometric health tracking including ECG, SpO2, and continuous heart monitoring.",
            "features": "1.92-inch Always-On OLED Retina Display | Aerospace Grade Titanium Case | 100m Water Resistance & Dive Ready | ECG, Blood Oxygen & Sleep Stage Tracking | Fast Magnetic Wireless Charging",
            "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80",
            "rating": 4.9,
            "rating_count": 42,
            "in_stock": True,
            "is_featured": True,
            "is_deal_of_the_day": True,
        },
        {
            "seller": seller1,
            "seller_name": "Apex Electronics Hub",
            "seller_contact": "arjun@apextech.com | +91 98765 11223",
            "product_name": "AcousticMaster ANC Wireless Headphones",
            "category": "Audio",
            "subcategory": "Headphones",
            "price": 8999,
            "original_price": 14499,
            "desc": "Immerse yourself in pure studio-grade acoustics. Powered by 40mm custom planar drivers, active hybrid noise cancellation, transparency mode, and 50 hours of wireless playback on a single charge.",
            "features": "Industry-Leading Hybrid Active Noise Cancellation | 40mm Custom Planar Acoustic Drivers | 50-Hour Extended Battery Life | Multipoint Bluetooth 5.3 & LDAC Codec | Ultra-Plush Memory Foam Ear Cushions",
            "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80",
            "rating": 4.8,
            "rating_count": 35,
            "in_stock": True,
            "is_featured": True,
            "is_deal_of_the_day": False,
        },
        {
            "seller": seller1,
            "seller_name": "Apex Electronics Hub",
            "seller_contact": "arjun@apextech.com | +91 98765 11223",
            "product_name": "CyberKey RGB Wireless Mechanical Keyboard",
            "category": "Electronics",
            "subcategory": "Computer Accessories",
            "price": 5499,
            "original_price": 7999,
            "desc": "Built for pro creators and gamers alike, CyberKey features hot-swappable tactile switches, CNC aluminum chassis, sound-dampening silicone gaskets, per-key RGB backlighting, and triple connectivity (2.4GHz, Bluetooth 5.0, USB-C).",
            "features": "Custom Hot-Swappable Tactile Mechanical Switches | Anodized CNC Aluminum Chassis | Gasket Mount Structure with Poron Sound Dampening | Per-Key South-Facing RGB Illumination | 4000mAh Battery (Up to 200h without RGB)",
            "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&auto=format&fit=crop&q=80",
            "rating": 4.7,
            "rating_count": 28,
            "in_stock": True,
            "is_featured": True,
            "is_deal_of_the_day": False,
        },
        {
            "seller": seller2,
            "seller_name": "Aura Luxury Fashion",
            "seller_contact": "sneha@aurafashion.in | +91 98112 33445",
            "product_name": "Monaco Italian Leather Biker Jacket",
            "category": "Fashion",
            "subcategory": "Outerwear",
            "price": 12499,
            "original_price": 18999,
            "desc": "Handcrafted from 100% full-grain Italian lambskin leather, the Monaco Jacket features asymmetrical antique silver YKK zippers, satin inner lining, quilted shoulder accents, and tailored silhouette that ages gracefully.",
            "features": "100% Full-Grain Premium Italian Lambskin | Heavy-Duty Antique Silver YKK Hardware | Breathable Silk-Finish Satin Interior Lining | Zippered Gusset Cuffs & Multiple Pockets | Hand-Waxed Weather-Resistant Finish",
            "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&auto=format&fit=crop&q=80",
            "rating": 4.9,
            "rating_count": 19,
            "in_stock": True,
            "is_featured": True,
            "is_deal_of_the_day": True,
        },
        {
            "seller": seller2,
            "seller_name": "Aura Luxury Fashion",
            "seller_contact": "sneha@aurafashion.in | +91 98112 33445",
            "product_name": "Velocity Air Runner Limited Edition Sneakers",
            "category": "Fashion",
            "subcategory": "Footwear",
            "price": 6999,
            "original_price": 9999,
            "desc": "Designed with aerodynamic contours, responsive nitrogen-infused foam midsoles, engineered breathable jacquard mesh, and high-traction carbon rubber outsoles for effortless streetwear appeal and athletic performance.",
            "features": "Nitrogen-Infused High Energy Return Cushioning | Seamless Engineered Breathable Mesh Upper | Reflective 3M Night-Vision Accents | Anatomical Arch Support Insole | Durable Anti-Slip Carbon Rubber Sole",
            "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&auto=format&fit=crop&q=80",
            "rating": 4.8,
            "rating_count": 56,
            "in_stock": True,
            "is_featured": False,
            "is_deal_of_the_day": False,
        },
        {
            "seller": seller2,
            "seller_name": "Aura Luxury Fashion",
            "seller_contact": "sneha@aurafashion.in | +91 98112 33445",
            "product_name": "Voyager Waterproof Modular Tech Backpack",
            "category": "Fashion",
            "subcategory": "Bags & Luggage",
            "price": 3899,
            "original_price": 5999,
            "desc": "Crafted from 1000D ballistic Cordura fabric with magnetic Fidlock buckles, dedicated 16-inch suspended laptop sleeve, hidden RFID passport pocket, and 28L expandable capacity for modern commuters and world travelers.",
            "features": "1000D Weatherproof Ballistic Cordura Fabric | Padded Suspended 16-inch Laptop Compartment | German Magnetic Fidlock Buckle System | Ergonomic Air-Mesh Shoulder Straps & Luggage Pass-Through | Hidden RFID-Blocking Anti-Theft Pocket",
            "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&auto=format&fit=crop&q=80",
            "rating": 4.6,
            "rating_count": 22,
            "in_stock": True,
            "is_featured": False,
            "is_deal_of_the_day": False,
        },
        {
            "seller": seller3,
            "seller_name": "Urban Lifestyle & Decor",
            "seller_contact": "vikram@urbanliving.in | +91 97788 55667",
            "product_name": "ErgoZen Pro Ergonomic Mesh Office Chair",
            "category": "Home & Living",
            "subcategory": "Furniture",
            "price": 16999,
            "original_price": 24999,
            "desc": "Engineered for 12+ hour comfort, ErgoZen features dynamic self-adjusting lumbar support, 4D multidirectional armrests, breathable high-tensile German mesh, Class-4 heavy duty gas lift, and 135-degree recline lock.",
            "features": "Dynamic Adaptive Lumbar Support System | German High-Tensile Breathable KRALL Mesh | 4D Multi-Angle Adjustable Armrests | 135° Recline with 3-Position Angle Lock | Heavy-Duty Aluminum Base (BIFMA Certified)",
            "image_url": "https://images.unsplash.com/photo-1580481077195-c3f25c7e3f89?w=800&auto=format&fit=crop&q=80",
            "rating": 4.9,
            "rating_count": 31,
            "in_stock": True,
            "is_featured": True,
            "is_deal_of_the_day": False,
        },
        {
            "seller": seller3,
            "seller_name": "Urban Lifestyle & Decor",
            "seller_contact": "vikram@urbanliving.in | +91 97788 55667",
            "product_name": "Nordic Minimalist Smart Ambient Desk Lamp",
            "category": "Home & Living",
            "subcategory": "Lighting",
            "price": 2799,
            "original_price": 4499,
            "desc": "An elegant blend of natural solid walnut wood and frosted anodized aluminum. Features 16-million color RGBW lighting, wireless phone charging base, touch dimming slider, and compatibility with Apple HomeKit & Alexa.",
            "features": "Integrated 15W Qi Fast Wireless Charging Base | 16 Million RGBW Colors + 2700K-6500K Warm/Cool White | Touch Stepless Brightness Control Slider | Smart App & Voice Control (Alexa/Google/HomeKit) | Natural Solid Walnut & Aluminum Craftsmanship",
            "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&auto=format&fit=crop&q=80",
            "rating": 4.7,
            "rating_count": 17,
            "in_stock": True,
            "is_featured": False,
            "is_deal_of_the_day": False,
        },
        {
            "seller": seller3,
            "seller_name": "Urban Lifestyle & Decor",
            "seller_contact": "vikram@urbanliving.in | +91 97788 55667",
            "product_name": "Barista Touch Compact Espresso Machine",
            "category": "Home & Living",
            "subcategory": "Kitchen Appliances",
            "price": 21999,
            "original_price": 28999,
            "desc": "Extract barista-quality espresso at home with 19-bar Italian ULKA pump pressure, thermo-block rapid heating system (ready in 25 seconds), precision PID temperature control, and commercial micro-foam steam wand for latte art.",
            "features": "19-Bar High-Pressure Italian Pump System | Thermo-Block Instant Heating in 25 Seconds | Commercial Grade 360° Stainless Steam Wand | Precision PID Digital Temperature Control | 1.8L Removable BPA-Free Water Reservoir",
            "image_url": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=800&auto=format&fit=crop&q=80",
            "rating": 4.8,
            "rating_count": 29,
            "in_stock": True,
            "is_featured": True,
            "is_deal_of_the_day": True,
        },
        {
            "seller": seller1,
            "seller_name": "Apex Electronics Hub",
            "seller_contact": "arjun@apextech.com | +91 98765 11223",
            "product_name": "SkyDrone 4K HDR GPS Quadcopter",
            "category": "Electronics",
            "subcategory": "Cameras & Drones",
            "price": 32999,
            "original_price": 42999,
            "desc": "Capture breathtaking cinematic vistas with 3-axis motorized gimbal stabilization, 4K/60fps HDR video recording, 38-minute flight endurance per battery, and 10km HD live video transmission with optical obstacle avoidance.",
            "features": "4K/60fps HDR Sensor with 3-Axis Mechanical Gimbal | 38-Minute Maximum Flight Time (Includes 2 Batteries) | 10km Full-HD Video Transmission Range | Omnidirectional Obstacle Sensing & Return-To-Home | Foldable Ultralight Carbon Fiber Arms",
            "image_url": "https://images.unsplash.com/photo-1527977966376-1c8408f9f108?w=800&auto=format&fit=crop&q=80",
            "rating": 4.9,
            "rating_count": 14,
            "in_stock": True,
            "is_featured": True,
            "is_deal_of_the_day": False,
        },
        {
            "seller": seller2,
            "seller_name": "Aura Luxury Fashion",
            "seller_contact": "sneha@aurafashion.in | +91 98112 33445",
            "product_name": "Aviator Classic Polarized Titanium Sunglasses",
            "category": "Fashion",
            "subcategory": "Accessories",
            "price": 3299,
            "original_price": 4999,
            "desc": "Timeless military aviator styling crafted with ultra-lightweight Japanese beta-titanium frames and Category 3 polarized mineral glass lenses with anti-reflective back coating.",
            "features": "Japanese Beta-Titanium Ultra-Lightweight Frame | 100% UV400 Protection & Hydrophobic Polarized Lenses | Anti-Reflective Interior Coating for Visual Clarity | Hypoallergenic Silicone Nose Pads | Hard Leather Storage Case Included",
            "image_url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&auto=format&fit=crop&q=80",
            "rating": 4.6,
            "rating_count": 24,
            "in_stock": True,
            "is_featured": False,
            "is_deal_of_the_day": False,
        },
        {
            "seller": seller3,
            "seller_name": "Urban Lifestyle & Decor",
            "seller_contact": "vikram@urbanliving.in | +91 97788 55667",
            "product_name": "Aromatherapy Ceramic Ultrasonic Diffuser",
            "category": "Home & Living",
            "subcategory": "Home Fragrance",
            "price": 1899,
            "original_price": 2999,
            "desc": "Handcrafted matte ceramic exterior with ultrasonic atomization technology. Releases a whisper-quiet fine fragrant mist that cleanses the air while illuminating your room with soft ambient candlelight.",
            "features": "Hand-Molded Matte Ceramic Stone Cover | Whisper-Quiet Ultrasonic Mist (Under 20dB) | Auto-Off Safety Protection When Water Runs Low | 7-Color Ambient Night Light Modes | 300ml Capacity (Up to 10 Hours Continuous)",
            "image_url": "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800&auto=format&fit=crop&q=80",
            "rating": 4.8,
            "rating_count": 18,
            "in_stock": True,
            "is_featured": False,
            "is_deal_of_the_day": False,
        }
    ]

    for pdata in products_data:
        p, created = Product.objects.update_or_create(
            product_name=pdata["product_name"],
            defaults=pdata
        )
        print(f"  - Product: {p.product_name} (₹{p.price}) [{'Created' if created else 'Updated'}]")

    # 3. Add Sample Reviews
    reviews_data = [
        {"product_name": "Apex Pro Ultra Smartwatch (OLED Titanium)", "user_name": "Karan Malhotra", "rating": 5, "comment": "Exceeded all my expectations! The titanium chassis feels exceptionally premium on the wrist, and battery easily lasts a full week with always-on display."},
        {"product_name": "Apex Pro Ultra Smartwatch (OLED Titanium)", "user_name": "Pooja Verma", "rating": 5, "comment": "Super accurate heart rate tracking and the screen is crystal clear even in direct sunlight. Seller Apex Tech shipped it in 24 hours."},
        {"product_name": "AcousticMaster ANC Wireless Headphones", "user_name": "Ananya Roy", "rating": 5, "comment": "The active noise cancellation is practically magic on flights. Soundstage is wide with punchy, controlled bass."},
        {"product_name": "AcousticMaster ANC Wireless Headphones", "user_name": "Dev Sharma", "rating": 4, "comment": "Great headphones for the price. Very comfortable ear cushions during long work sessions."},
        {"product_name": "Monaco Italian Leather Biker Jacket", "user_name": "Siddharth Rao", "rating": 5, "comment": "Pure luxury leather. The smell, the texture, and the fit are unmatched. Worth every single rupee."},
        {"product_name": "ErgoZen Pro Ergonomic Mesh Office Chair", "user_name": "Meera Nambiar", "rating": 5, "comment": "Completely cured my lower back pain after long 10-hour coding sessions. Best chair in this segment."}
    ]

    for rdata in reviews_data:
        try:
            prod = Product.objects.get(product_name=rdata["product_name"])
            Review.objects.get_or_create(
                product=prod,
                user_name=rdata["user_name"],
                defaults={"rating": rdata["rating"], "comment": rdata["comment"]}
            )
            prod.update_rating()
        except Product.DoesNotExist:
            pass

    print("✅ Product reviews seeded")

    # 4. Create Blog Posts
    blog_posts_data = [
        {
            "author_user": admin_user,
            "title": "The Future of E-Commerce: AI, Personalization & What's Coming Next",
            "slug": "future-of-ecommerce-ai-personalization-2025",
            "author": "Arjun Sharma",
            "author_role": "Senior Tech Editor",
            "author_avatar": "A",
            "category": "Technology",
            "tags": "AI, E-Commerce, Future Trends, Shopping",
            "read_time": "8 min read",
            "excerpt": "Artificial intelligence is reshaping how consumers shop online. From personalized recommendations that anticipate your needs to hyper-realistic virtual try-ons, discover what the next generation of commerce looks like.",
            "content": """The retail landscape is undergoing a monumental paradigm shift. What began as simple online catalog shopping has matured into an intelligent, immersive digital ecosystem driven by modern AI architectures and real-time behavioral personalization.

### The Rise of Hyper-Personalized Discovery
In the early days of e-commerce, search and categorization were static. Today, neural recommenders analyze nuance, contextual intent, and purchase lifecycles to surface products you genuinely care about at the exact right moment.

Rather than wading through hundreds of irrelevant listings, buyers encounter tailored storefronts that evolve with their preferences. This frictionless journey dramatically reduces purchase anxiety and enhances overall satisfaction.

### Virtual Try-Ons & Augmented Reality
One of the most persistent bottlenecks in online shopping has been the uncertainty of fit and material feel. Augmented reality tools now allow shoppers to project 3D furniture models into their living rooms with millimetric accuracy, or virtually preview how a leather jacket fits their proportions before hitting checkout.

### Decentralized Peer-to-Peer Marketplaces
Modern platforms are empowering individual artisans, boutique creators, and independent sellers to reach consumers directly without predatory middleman fees. S_Cart's open seller ecosystem enables anyone to list premium gear, build a following, and communicate directly with buyers through instant product inquiries.

The future belongs to platforms that prioritize authenticity, high craft, and genuine human connection. As technology continues to accelerate, the lines between physical browsing and digital convenience will continue to dissolve.""",
            "thumbnail_url": "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=1200&auto=format&fit=crop&q=80",
            "icon": "🤖",
            "is_featured": True,
            "views": 348
        },
        {
            "author_user": seller2,
            "title": "Sustainable Fashion: How to Build a Timeless Capsule Wardrobe",
            "slug": "sustainable-fashion-capsule-wardrobe-guide",
            "author": "Sneha Patel",
            "author_role": "Fashion Director & Stylist",
            "author_avatar": "S",
            "category": "Fashion",
            "tags": "Fashion, Sustainability, Minimalist, Style Guide",
            "read_time": "6 min read",
            "excerpt": "Fast fashion is fading in favor of durable, high-craft staples. Here is our master guide to curating a 15-piece capsule wardrobe that looks pristine in any setting.",
            "content": """Fast fashion has spent the last decade flooding closets with disposable garments designed to disintegrate after five washes. Today's conscious shopper is rejecting that cycle in favor of timeless, ethically produced quality.

### What is a Capsule Wardrobe?
A capsule wardrobe is a curated collection of versatile, premium essentials that coordinate effortlessly. Instead of owning 80 mediocre pieces, you invest in 15 to 20 exceptional items that can be mixed and matched across seasons.

### Key Pillars of a Modern Capsule:
1. **The Statement Outerwear:** A genuine full-grain leather jacket or tailored wool overcoat that elevates even the simplest white tee.
2. **Premium Everyday Footwear:** Clean leather sneakers or Goodyear-welted boots that deliver all-day comfort and age gracefully.
3. **Structured Breathable Basics:** Heavyweight organic cotton t-shirts and tailored trousers in versatile neutral palettes (charcoal, navy, beige, and black).

By investing in enduring craftsmanship, you not only reduce ecological impact — you save thousands of hours and look consistently confident every morning.""",
            "thumbnail_url": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=1200&auto=format&fit=crop&q=80",
            "icon": "👗",
            "is_featured": False,
            "views": 215
        },
        {
            "author_user": seller1,
            "title": "Audiophile Breakdown: Why Planar Magnetic Drivers Are Dominating 2025",
            "slug": "audiophile-breakdown-planar-magnetic-drivers",
            "author": "Arjun Sharma",
            "author_role": "Audio Engineer & Reviewer",
            "author_avatar": "A",
            "category": "Audio",
            "tags": "Audio, Headphones, Acoustics, Hardware",
            "read_time": "7 min read",
            "excerpt": "Curious why high-end headphones are ditching standard dynamic cones for ultra-thin planar diaphragms? Here is what happens to your music when distortion drops to near zero.",
            "content": """If you have ever listened to your favorite track through a pair of planar magnetic headphones, you already know the sensation: suddenly you hear the subtle breath of the vocalist, the delicate scrape of fingers sliding across acoustic guitar strings, and bass that extends down into sub-audible frequencies with zero distortion.

### How Planar Magnetic Drivers Work
Traditional headphones use a conical diaphragm attached to a copper voice coil that pushes air from the center. This often introduces harmonic distortion at high volume.

Planar magnetic drivers instead suspend an ultra-thin conductive film between opposing magnetic arrays. The electromagnetic force is distributed evenly across the entire surface of the diaphragm, moving air uniformly with lightning-fast transient response.

The result is breathtaking instrument separation and an open soundstage that makes you feel as though you are sitting in the direct center of the recording studio.""",
            "thumbnail_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=1200&auto=format&fit=crop&q=80",
            "icon": "🎧",
            "is_featured": False,
            "views": 182
        },
        {
            "author_user": seller3,
            "title": "Designing a High-Performance Desk Setup for Remote Focus",
            "slug": "designing-high-performance-desk-setup-remote-work",
            "author": "Vikram Nair",
            "author_role": "Ergonomics Consultant",
            "author_avatar": "V",
            "category": "Lifestyle",
            "tags": "Desk Setup, Ergonomics, Productivity, Home Office",
            "read_time": "5 min read",
            "excerpt": "Working from home shouldn't compromise your spine or sanity. Simple modifications in lighting, posture, and acoustics can double your deep work capacity.",
            "content": """Your workspace is the physical cockpit for your cognitive output. When your chair offers poor lumbar support or your desk lighting causes harsh screen glare, your brain expends subtle energy compensating for physical fatigue.

### The 90-Degree Ergonomic Golden Rule
Your elbows, hips, and knees should rest comfortably at 90-degree angles. Invest in an adjustable mesh office chair with active lumbar support like the ErgoZen Pro, ensuring your feet rest flat on the floor and your forearms align parallel with your desk surface.

### Layered Indirect Lighting
Never work in pitch darkness with only a bright computer monitor glaring in your eyes. Combine warm bias lighting behind your display with an adjustable smart desk lamp (2700K to 4000K warm white) to eliminate eye strain during evening focus blocks.

A clean, intentional workspace transforms routine tasks into enjoyable, focused flow states.""",
            "thumbnail_url": "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=1200&auto=format&fit=crop&q=80",
            "icon": "🏠",
            "is_featured": False,
            "views": 290
        }
    ]

    for bdata in blog_posts_data:
        bp, created = BlogPost.objects.update_or_create(
            slug=bdata["slug"],
            defaults=bdata
        )
        print(f"  - BlogPost: {bp.title} [{'Created' if created else 'Updated'}]")

    # 5. Add Sample Blog Comments
    try:
        post1 = BlogPost.objects.get(slug="future-of-ecommerce-ai-personalization-2025")
        BlogComment.objects.get_or_create(
            post=post1,
            name="Rohan Kapur",
            email="rohan@techcrunch.com",
            defaults={"comment": "Fascinating analysis! Especially agree on the impact of decentralized marketplace models allowing independent creators to connect directly with buyers."}
        )
        BlogComment.objects.get_or_create(
            post=post1,
            name="Divya Singhania",
            email="divya@designstudio.in",
            defaults={"comment": "The virtual try-on tech mentioned here is already making such a massive difference in returns. Great read!"}
        )
    except BlogPost.DoesNotExist:
        pass

    # 6. Create Sample Orders & Updates
    sample_order, o_created = Order.objects.get_or_create(
        order_id="SC-2024-48291",
        defaults={
            "user": buyer1,
            "name": "Rohit Kumar",
            "email": "rohit.k@gmail.com",
            "phone": "+91 98765 43210",
            "address": "Flat 402, Lotus Residency, 100 Feet Road, Indiranagar",
            "city": "Bengaluru",
            "state": "Karnataka",
            "zip_code": "560038",
            "items_json": '[{"name": "Apex Pro Ultra Smartwatch (OLED Titanium)", "qty": 1, "price": 14999}, {"name": "Voyager Waterproof Modular Tech Backpack", "qty": 1, "price": 3899}]',
            "amount": 22300,
            "status": "In Transit",
            "payment_method": "UPI",
            "payment_status": "Completed",
            "courier": "BlueDart Express",
            "tracking_number": "BD9823471029"
        }
    )

    if o_created:
        OrderUpdate.objects.create(order=sample_order, update_desc="Package in transit - Hub Bengaluru Outer Ring Road")
        OrderUpdate.objects.create(order=sample_order, update_desc="Dispatched from Warehouse via BlueDart Express")
        OrderUpdate.objects.create(order=sample_order, update_desc="Order placed successfully and payment verified via UPI")

    # 7. Create Sample Product Inquiries
    sample_prod = Product.objects.filter(seller=seller1).first()
    if sample_prod:
        ProductInquiry.objects.get_or_create(
            product=sample_prod,
            name="Sameer Joshi",
            email="sameer.j@outlook.com",
            phone="+91 99887 66554",
            defaults={
                "subject": f"Warranty & Compatibility Inquiry for {sample_prod.product_name}",
                "message": "Hi Arjun, does this model support iOS 18 call notifications and does it come with 1-year manufacturer warranty? Looking to order 2 units."
            }
        )

    print("🎉 Database seeded successfully with real products, sellers, blog articles, comments, inquiries, and orders!")

if __name__ == '__main__':
    seed()
