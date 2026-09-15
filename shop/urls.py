from django.urls import path
from . import views

urlpatterns = [
    # Core Shop Pages
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="ShopAbout"),
    path("contact/", views.contact, name="ShopContact"),
    path("tracker/", views.tracker, name="ShopTracker"),
    path("search/", views.search, name="ShopSearch"),
    path("products/<int:myid>/", views.productView, name="ShopProductView"),
    path("products/<int:myid>/inquiry/", views.product_inquiry, name="ShopProductInquiry"),
    path("products/<int:myid>/review/", views.add_review, name="ShopAddReview"),
    path("checkout/", views.checkout, name="ShopCheckout"),
    path("order-success/<str:order_id>/", views.order_success, name="ShopOrderSuccess"),

    # Auth & Seller Dashboard
    path("register/", views.register_view, name="ShopRegister"),
    path("login/", views.login_view, name="ShopLogin"),
    path("logout/", views.logout_view, name="ShopLogout"),
    path("dashboard/", views.dashboard_view, name="ShopDashboard"),
    path("products/add/", views.add_product_view, name="ShopAddProduct"),
    path("products/edit/<int:myid>/", views.edit_product_view, name="ShopEditProduct"),
    path("products/delete/<int:myid>/", views.delete_product_view, name="ShopDeleteProduct"),
    path("inquiry/mark-read/<int:inquiry_id>/", views.mark_inquiry_read, name="ShopMarkInquiryRead"),

    # Cart AJAX APIs
    path("api/cart/", views.api_get_cart, name="ShopApiCart"),
    path("api/cart/add/", views.api_add_to_cart, name="ShopApiCartAdd"),
    path("api/cart/update/", views.api_update_cart, name="ShopApiCartUpdate"),
    path("api/cart/clear/", views.api_clear_cart, name="ShopApiCartClear"),

    # Legacy callbacks
    path("handlerequest/", views.handlerequest, name="ShopHandleRequest"),
    path("paymenthandler/", views.paymenthandler, name="ShopPaymentHandler"),
]
