from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register((Maincategory,Subcategory,Wishlist,Brands,Product,Buyer,Checkout,CheckoutProducts,Support_Querry))
