"""
URL configuration for azone_clone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('', views.index, name='index'), # Home page view
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.CartProduct, name='cart_page'),
    path('remove-from-cart/<int:item_id>/', views.Remove_form_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add_product/', views.add_product, name='add_product'),
    path('search/', views.search_view, name='search'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add_review/<int:product_id>/', views.add_review, name='add_review'),
    path('logout/', views.logout_view, name='logout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('category/<str:name>/', views.category_products, name='category_products'),
]
