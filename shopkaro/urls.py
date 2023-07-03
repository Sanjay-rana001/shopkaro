
from django.contrib import admin
from django.urls import path
from Mainapp import views as mainapp
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainapp.homepage),
    path('loginpage/', mainapp.loginpage),
    path('logoutpage/', mainapp.logoutpage),
    path('forgetPassword1/', mainapp.forgetPassword1),
    path('forgetPassword2/', mainapp.forgetPassword2),
    path('forgetPassword3/', mainapp.forgetPassword3),
    path('registerpage/', mainapp.registerpage),
    path('cart/', mainapp.cartpage),
    path('addTocart/<int:num>/', mainapp.addTocart),
    path('addTowishlist/<int:num>/', mainapp.addTowishlist),
    path('removeFromcart/<str:num>/', mainapp.removeFromcart),
     path('update-cart/<str:num>/<str:op>/',mainapp.updateCartPage),
    path('removeFromwishlist/<str:num>/', mainapp.removeFromwishlist), 
    path('profile/', mainapp.profilepage),
    path('update_profile/', mainapp.update_profilepage),

    path('blog/', mainapp.blogpage),
    path('supportForm/', mainapp.supportForm),
    path('contact/', mainapp.contactpage),
    path('product/<str:mc>/<str:sc>/<str:br>/', mainapp.productpage),
    path('price-filter/<str:mc>/<str:sc>/<str:br>/', mainapp.pricefilterpage),
    path('color-filter/<str:mc>/<str:sc>/<str:br>/', mainapp.colorfilterpage),
    path('testimonial/', mainapp.testimonialpage),
    path('search/', mainapp.searchpage),
    path('checkout/', mainapp.checkoutpage),
    path('place-order/', mainapp.place_order), 
    path('paymentSuccess/<str:rppid>/<str:rpoid>/<str:rpsid>/<int:checkid>/', mainapp.paymentSuccess),
    path('re-payment/<int:checkid>/', mainapp.payAgain),
    path('confirmation/', mainapp.confirmationpage),
    path('filter/<str:mc>/<str:sc>/<str:br>/<str:filter>/', mainapp.filterpage),
    path('product_detail/<int:num>/', mainapp.product_deatail)
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
