from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Consumer routes
    path('consumer/dashboard/', views.consumer_dashboard, name='consumer_dashboard'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order/place/', views.place_order, name='place_order'),

    # Farmer routes
    path('farmer/dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('farmer/edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('farmer/product/add/', views.add_product, name='add_product'),
    path('farmer/product/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    path('checkout/', views.checkout, name='checkout'),
    path('payment/process/', views.process_payment, name='process_payment'),
    path('payment/success/<str:txid>/', views.payment_success, name='payment_success'),
    path('orders/', views.consumer_orders, name='consumer_orders'),
]
