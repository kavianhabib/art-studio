from django.urls import path
from .views import ( CheckoutView, product, HomeView, 
ItemDetailView, add_to_cart,remove_from_cart,OrderSummaryView, remove_single_item_from_cart,
PaymentView,MyProductsView, AboutView, ContactView)

app_name = 'core'

urlpatterns =[
    path('', HomeView.as_view(), name = 'home'),
    path('checkout/<slug>', CheckoutView.as_view(), name = 'checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name = 'order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name = 'product'),
    path('add-to-cart/<slug>/', add_to_cart, name = 'add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name = 'remove-from-cart'),
    path('remove-single-itemfrom-cart/<slug>/', remove_single_item_from_cart, name = 'remove-single-item-from-cart'),
    # path('payment/<payment_option>', PaymentView.as_view(), name = 'payment'),
    path('payment/', PaymentView.as_view(), name = 'payment'),
    path('my-products', MyProductsView.as_view(), name = 'my-products'),
    path('about', AboutView.as_view(), name = 'about'),
    path('contact', ContactView.as_view(), name = 'contact'),
] 