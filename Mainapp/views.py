from django.shortcuts import render,HttpResponseRedirect
from .models import *
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from shopkaro.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
import razorpay 



# Create your views here.

def homepage(request):
    # request.session.flush()
    cart = request.session.get("cart",None)
    product = Product.objects.all().order_by("id")[:75:15]
    data = Product.objects.all().order_by("base_price")[:9]
    brands = Brands.objects.all()
    
    return render(request,"index.html",{"data":data,"product":product,"brands":brands ,"cart":cart}) 

def loginpage(request):
    if(request.method=="POST"):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username,password=password)
        if (user is None):
            messages.error(request, "invalid Username or Password")
        else:
            
            auth.login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect("/admin/")  
            else:
                return HttpResponseRedirect("/profile/")
    brands = Brands.objects.all()

    return render(request,"loginform.html",{"brands":brands})

def logoutpage(request):
    auth.logout(request)
    return HttpResponseRedirect("/loginpage/")


def registerpage(request):
    a = User.objects.all()
    if(request.method=="POST"):
        
        if(request.POST.get("pass1")!= request.POST.get("pass2")):
            messages.error(request, "OOPS!! Password does not matched")
        else:
            try:
               user = User.objects.create(username=request.POST.get("user_name"))
               user.set_password (request.POST.get("pass1"))
               user. save()
   
               b = Buyer()
               b.name = request.POST.get("Fname")
               b.username = request.POST.get("user_name")
               b.email = request.POST.get("usermail")
               b.phone = request.POST.get("phone")
               b.save()

               subject = 'Your Account has been created: Team Shopkaro'
               message = f"""Hi {b.username}, your account has been creadted successfully
                             Don"t miss out the latest deal.. grab soon
                             Team:Shopkaro."""
               email_from = settings.EMAIL_HOST_USER
               recipient_list = [b.email, ]
               send_mail( subject, message, email_from, recipient_list )
               return HttpResponseRedirect("/loginpage/")
            except:
               messages.error(request,"Username Already Taken!!!")
    brands = Brands.objects.all()          
    return render(request,"registerform.html",{"brands":brands})


@login_required(login_url="/loginpage/")
def profilepage(request):
    brands = Brands.objects.all()
    user = User.objects.get(username=request.user.username)
    if (user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        buyer = Buyer.objects.get(username= request.user.username) 
        wishlist = Wishlist.objects.filter(buyer = buyer)
        checkout = Checkout.objects.filter(buyer= buyer)
        orders = []
        for item in checkout:
            cp = CheckoutProducts.objects.filter(checkout = item.id)
            orders.append({"checkout":item,"checkoutProducts":cp})
            
    return render(request, "profile.html" ,{"data":buyer ,"brands":brands ,"wishlist":wishlist,"orders":orders })
    

@login_required(login_url="/loginpage/") 
def update_profilepage(request):
    brands = Brands.objects.all()   
    user = User.objects.get(username=request.user.username)
    
    if (user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        buyer = Buyer.objects.get(username= request.user.username) 
        if(request.method=="POST"):
            b = buyer
            b.name = request.POST.get("Fname")
            b.email = request.POST.get("usermail")
            b.phone = request.POST.get("phone")
            b.addressline1 = request.POST.get("adress1")
            b.addressline2 = request.POST.get("adress2")
            b.addressline3 = request.POST.get("adress3")
            b.city = request.POST.get("city")
            b.state = request.POST.get("state")
            b.pin = request.POST.get("pincode")
            if(request.FILES.get("pic") !=None):
                b.pic = request.FILES.get("pic")
            b.save()    
            return HttpResponseRedirect("/profile/")
    return render(request,"update_profile.html",{"data":buyer, "brands":brands}) 

 


def blogpage(request):
    return render(request,"blog_list.html") 

 
def contactpage(request):
    return render(request,"contact.html")  



# -------------Product filters------------------>

# product with categories
def productpage(request,mc,sc,br):
    if (mc=="All") and (sc=="All") and (br=="All"):
        data = Product.objects.all().order_by("-id")
    elif (mc!="All") and (sc=="All") and (br=="All"):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc)).order_by("-id")
    elif (mc=="All") and (sc!="All") and (br=="All"): 
        data = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc)).order_by("-id")
    elif (mc=="All") and (sc=="All") and (br!="All"):
        data = Product.objects.filter(brands=Brands.objects.get(name=br)).order_by("-id")
    elif (mc!="All") and (sc!="All") and (br=="All"):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc)).order_by("-id")
    elif (mc!="All") and (sc=="All") and (br!="All"): 
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brands=Brands.objects.get(name=br)).order_by("-id")   
    elif (mc=="All") and (sc!="All") and (br!="All"):
        data = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc),brands=Brands.objects.get(name=br)).order_by("-id")
    else:    
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc),brands=Brands.objects.get(name=br)).order_by("-id")
    product = Product.objects.all().order_by("id")[:75:15]
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brands = Brands.objects.all()
    return render(request,"product.html",{"data":data,"product":product,"maincategory":maincategory,"subcategory":subcategory,"brands":brands,"mc":mc,"sc":sc,"br":br}) 


# product with sorting filters

def filterpage(request,mc,sc,br,filter):
    if(filter=="Latest"): 
        if (mc=="All") and (sc=="All") and (br=="All"):
           data = Product.objects.all().order_by("-id")
        elif (mc!="All") and (sc=="All") and (br=="All"):
           data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc)).order_by("-id")
        elif (mc=="All") and (sc!="All") and (br=="All"): 
           data = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc)).order_by("-id")
        elif (mc=="All") and (sc=="All") and (br!="All"):
           data = Product.objects.filter(brands=Brands.objects.get(name=br)).order_by("-id")
        elif (mc!="All") and (sc!="All") and (br=="All"):
           data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc)).order_by("-id")
        elif (mc!="All") and (sc=="All") and (br!="All"): 
           data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brands=Brands.objects.get(name=br)).order_by("-id")   
        elif (mc=="All") and (sc!="All") and (br!="All"):
           data = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc),brands=Brands.objects.get(name=br)).order_by("-id")
        else:    
           data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc),brands=Brands.objects.get(name=br)).order_by("-id") 

    elif(filter=="LtoH"): 
        if (mc=="All") and (sc=="All") and (br=="All"):
           data = Product.objects.all().order_by("final_price")
        elif (mc!="All") and (sc=="All") and (br=="All"):
           data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc)).order_by("final_price")
        elif (mc=="All") and (sc!="All") and (br=="All"): 
           data = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc)).order_by("final_price")
        elif (mc=="All") and (sc=="All") and (br!="All"):
           data = Product.objects.filter(brands=Brands.objects.get(name=br)).order_by("final_price")
        elif (mc!="All") and (sc!="All") and (br=="All"):
           data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc)).order_by("final_price")
        elif (mc!="All") and (sc=="All") and (br!="All"): 
           data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brands=Brands.objects.get(name=br)).order_by("final_price")   
        elif (mc=="All") and (sc!="All") and (br!="All"):
           data = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc),brands=Brands.objects.get(name=br)).order_by("final_price")
        else:    
           data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc),brands=Brands.objects.get(name=br)).order_by("final_price") 
    else: 
        if (mc=="All") and (sc=="All") and (br=="All"):
           data = Product.objects.filter().order_by("-final_price")
        elif (mc!="All") and (sc=="All") and (br=="All"):
           data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc)).order_by("-final_price")
        elif (mc=="All") and (sc!="All") and (br=="All"): 
           data = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc)).order_by("-final_price")
        elif (mc=="All") and (sc=="All") and (br!="All"):
           data = Product.objects.filter(brands=Brands.objects.get(name=br)).order_by("-final_price")
        elif (mc!="All") and (sc!="All") and (br=="All"):
           data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc)).order_by("-final_price")
        elif (mc!="All") and (sc=="All") and (br!="All"): 
           data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brands=Brands.objects.get(name=br)).order_by("-final_price")   
        elif (mc=="All") and (sc!="All") and (br!="All"):
           data = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc),brands=Brands.objects.get(name=br)).order_by("-final_price")
        else:    
           data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc),brands=Brands.objects.get(name=br)).order_by("-final_price")               

    product = Product.objects.all().order_by("id")[:75:15]
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brands = Brands.objects.all()
    return render(request,"product.html",{"data":data,"product":product,"maincategory":maincategory,"subcategory":subcategory,"brands":brands,"mc":mc,"sc":sc,"br":br}) 
  
#  product with price filter 

def pricefilterpage(request,mc,sc,br):

    option = request.POST.get("price")
    min = 0
    max = 100000
    if(option=="1"):
        min = 0
        max = 100000
    elif(option=="2"):
        min = 0
        max = 1000
    elif(option=="3"):
        min = 1000
        max = 2000    
    elif(option=="4"):
        min = 2000
        max = 3000
    elif(option=="5"):
        min = 3000
        max = 4000      
    elif(option=="6"):
        min = 4000
        max = 5000
    elif(option=="7"):
        min = 5000
        max = 100000          

    if (mc=="All") and (sc=="All") and (br=="All"):
        data = Product.objects.filter(final_price__gte=min,final_price__lte=max).order_by("final_price") 
    elif (mc!="All") and (sc=="All") and (br=="All"):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),final_price__gte=min,final_price__lte=max,).order_by("final_price")
    elif (mc=="All") and (sc!="All") and (br=="All"): 
        data = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc),final_price__gte=min,final_price__lte=max).order_by("final_price")
    elif (mc=="All") and (sc=="All") and (br!="All"):
        data = Product.objects.filter(brands=Brands.objects.get(name=br),final_price__gte=min,final_price__lte=max).order_by("final_price")
    elif (mc!="All") and (sc!="All") and (br=="All"):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc),final_price__gte=min,final_price__lte=max).order_by("final_price")
    elif (mc!="All") and (sc=="All") and (br!="All"): 
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brands=Brands.objects.get(name=br),final_price__gte=min,final_price__lte=max).order_by("final_price")   
    elif (mc=="All") and (sc!="All") and (br!="All"):
        data = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc),brands=Brands.objects.get(name=br),final_price__gte=min,final_price__lte=max).order_by("final_price")
    else:    
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc),brands=Brands.objects.get(name=br),final_price__gte=min,final_price__lte=max).order_by("final_price")
    product = Product.objects.all().order_by("id")[:75:15]
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brands = Brands.objects.all()
    return render(request,"product.html",{"data":data,"product":product,"maincategory":maincategory,"subcategory":subcategory,"brands":brands,"mc":mc,"sc":sc,"br":br})


def colorfilterpage(request,mc,sc,br):

    option = request.POST.get("color")

    if(option=="1"):
        clr = "null"
    elif(option=="2"):
        clr = "Black" 
    elif(option=="3"):
        clr = "White"
    elif(option=="4"):
        clr = "Red"  
    elif(option=="5"):
         clr = "Blue"
    elif(option=="6"):
         clr = "Green"
    elif(option=="7"):
         clr = "Yellow"    
    

   
    if (mc=="All") and (sc=="All") and (br=="All"):
        data = Product.objects.filter(color=clr).order_by("final_price") 
    elif (mc!="All") and (sc=="All") and (br=="All"):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),color=clr,).order_by("final_price")
    elif (mc=="All") and (sc!="All") and (br=="All"): 
        data = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc),color=clr).order_by("final_price")
    elif (mc=="All") and (sc=="All") and (br!="All"):
        data = Product.objects.filter(brands=Brands.objects.get(name=br),color=clr).order_by("final_price")
    elif (mc!="All") and (sc!="All") and (br=="All"):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc),color=clr).order_by("final_price")
    elif (mc!="All") and (sc=="All") and (br!="All"): 
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brands=Brands.objects.get(name=br),color=clr).order_by("final_price")   
    elif (mc=="All") and (sc!="All") and (br!="All"):
        data = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc),brands=Brands.objects.get(name=br),color=clr).order_by("final_price")
    else:    
        data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc),brands=Brands.objects.get(name=br),color=clr).order_by("final_price")
    product = Product.objects.all().order_by("id")[:75:15]
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brands = Brands.objects.all()
    return render(request,"product.html",{"data":data,"product":product,"maincategory":maincategory,"subcategory":subcategory,"brands":brands,"mc":mc,"sc":sc,"br":br})


def searchpage(request):
   if(request.method=="POST"):
       search = request.POST.get("search")
       data = Product.objects.filter(Q(name__contains=search)|Q(color__contains=search)|Q(size__contains=search)|Q(stock__contains=search)|Q(description__contains=search)|Q(maincategory__name__contains=search)|Q(brands__name__contains=search)|Q(subcategory__name__contains=search))
       product = Product.objects.all().order_by("id")[:75:15]
       maincategory = Maincategory.objects.all()
       subcategory = Subcategory.objects.all()
       brands = Brands.objects.all()
       return render(request,"product.html",{"data":data,"product":product,"maincategory":maincategory,"subcategory":subcategory,"brands":brands,"mc":"All","sc":"All","br":"All"})
   else:
       return HttpResponseRedirect("/")


def testimonialpage(request):
    return render(request,"testimonial.html") 

def product_deatail(request,num):
   
    product = Product.objects.all().order_by("id")[:75:20]
    data = Product.objects.get(id=num)
    return render(request,"product_detail.html",{"data":data,"product":product ,} )




@login_required(login_url="/loginpage/")
def cartpage(request):
    cart = request.session.get("cart",None)
    print(cart,"\n\n\n\n\n")
    return render(request,"cart.html", {"cart":cart}) 


def addTocart(request,num):
    p = Product.objects.get(id=num)
    if(p):
        cart = request.session.get("cart",None)
        if(cart):
            if(str(num) in cart) :
                return HttpResponseRedirect("/cart/")
            else:
                cart.setdefault(str(num),{"id":p.id,
                                 "name":p.name,
                                 "brand":p.brands.name,
                                 "subcategory":p.subcategory.name,
                                 "color":p.color,
                                 "size":p.size,
                                 "price":p.final_price,
                                 "Qty":1,
                                 "total":p.final_price,
                                 "pic":p.pic1.url })
        else:
            cart = {str(num):{"id":p.id,
                                 "name":p.name,
                                 "brand":p.brands.name,
                                 "subcategory":p.subcategory.name,

                                 "color":p.color,   
                                 "size":p.size,
                                 "price":p.final_price,
                                 "Qty":1,
                                 "total":p.final_price,
                                 "pic":p.pic1.url }}
        subtotal = 0
        count = 0
        for key,value in cart.items():
            subtotal = subtotal+value["total"]
            count = count+value["Qty"]
        if (subtotal>0 and subtotal<1000):
            shipping = 150
        else: 
            shipping = 0     
        total = subtotal+shipping

        request.session["cart"] = cart       
        request.session["subtotal"] =  subtotal          
        request.session["shipping"] = shipping         
        request.session["total"] = total         
        request.session["count"]= count       
        request.session.set_expiry(60*60*24*31) 
        return HttpResponseRedirect("/cart/")

    else:
        return HttpResponseRedirect("/product/All/All/All/")
    

def removeFromcart(request,num):
    cart = request.session.get("cart",None)
    if(cart and num in cart):
        del cart[num]
        request.session["cart"] = cart
        subtotal = 0
        count = 0
        for key,value in cart.items():
            subtotal = subtotal+value["total"]
            count = count+value["Qty"]
        if (subtotal>0 and subtotal<1000):
            shipping = 150
        else: 
            shipping = 0      
        total = subtotal+shipping

        request.session["cart"] = cart       
        request.session["subtotal"] =  subtotal          
        request.session["shipping"] = shipping         
        request.session["total"] = total         
        request.session["count"]= count
    return HttpResponseRedirect("/cart/")    



def updateCartPage(Request,num,op):
    cart = Request.session.get("cart",None)
    if(cart and num in cart):
        item = cart[num]
        if(item['Qty']==1 and op=="Dec"):
            return HttpResponseRedirect("/cart/")
        elif(op=="Dec"):
            item['Qty'] = item['Qty']-1
            item['total'] = item['total']-item['price']
        else:
            item['Qty'] = item['Qty']+1
            item['total'] = item['total']+item['price']
        Request.session['cart']=cart
        subtotal = 0
        count = 0
        for key,values in cart.items():
            subtotal = subtotal+values['total']
            count = count + values['Qty']
        if(subtotal>0 and subtotal<1000):
            shipping = 150
        else:
            shipping =  0
        total = subtotal + shipping
        Request.session['cart']=cart        
        Request.session['subtotal']=subtotal        
        Request.session['shipping']=shipping        
        Request.session['total']=total        
        Request.session['count']=count
        Request.session.set_expiry(60*60*24*30)
    return HttpResponseRedirect("/cart/")



@login_required(login_url="/loginpage/")
def addTowishlist(request,num):
    try:
        p = Product.objects.get(id = num)
        buyer = Buyer.objects.get(username = request.user.username)
        try:
            wishlist = Wishlist.objects.get(buyer=buyer,product=p)
        except:
            w = Wishlist()   
            w.buyer = buyer
            w.product = p
            w.save()
    except:
        pass          
    return HttpResponseRedirect("/profile/")   

 
@login_required(login_url="/loginpage/")
def removeFromwishlist(request,num):
    try:
        item = Wishlist.objects.get(id=num)
        item.delete()
        
    except:
        pass   
    return HttpResponseRedirect("/profile/")



@login_required(login_url="/loginpage/")
def checkoutpage(request):
    try:
         buyer = Buyer.objects.get(username= request.user.username) 
         return render(request,"checkout.html",{"buyer":buyer}) 
    except:
        return HttpResponseRedirect("/cart/")



client=razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))
@login_required(login_url="/loginpage/")    
def place_order(request):
    if (request.method=="POST"):
        buyer = Buyer.objects.get(username = request.user.username)
        mode = request.POST.get("mode")
        subtotal = request.session.get("subtotal",0)
        shipping = request.session.get("shipping",0)
        total = request.session.get("total",0)
        if(subtotal==0):
            return HttpResponseRedirect("/checkout/")
        
        check = Checkout()
        check.buyer = buyer 
        check.subtotal = subtotal 
        check.shipping = shipping 
        check.final =  total
        check.save()
        
        cart = request.session.get("cart",None)
        for key,values in cart.items():
            p = Product.objects.get(id=(int(key)))
            cp = CheckoutProducts()
            cp.checkout = check  
            cp.product = p 
            cp.qty= values["Qty"]
            cp.total= values["total"]
            cp.save()

        request.session["cart"] = {}    
        request.session["subtotal"] = 0    
        request.session["shipping"] = 0    
        request.session["total"] = 0    
        request.session["count"] = 0

        if(mode=="COD"):
            
            subject = 'Order has been placed : Team Shopkaro'
            message = f"""Hi {buyer.name}, Your order  has been placed with order id {p.id}
                          kindly track you order in profile section 
                          Team:Shopkaro."""
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [buyer.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return HttpResponseRedirect("/confirmation/")
        else:
            orderAmount = check.final*100
            orderCurrency = "INR"
            paymentOrder = client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))
            paymentId=paymentOrder["id"]
            check.paymentMode = 2
            check.paymentStatus=2

            check.save()      
            return render(request,"pay.html",{
                "amount":orderAmount,
                "api_key":RAZORPAY_API_KEY,
                "order_id":paymentId,
                "User":buyer,
                "checkid":9999999999
            })    
    else:
        return HttpResponseRedirect("/checkout/")



@login_required(login_url="/loginpage/")    
def paymentSuccess(request,rppid,rpoid,rpsid,checkid):
        buyer = Buyer.objects.get(username = request.user)
        if(checkid==9999999999):
            check = Checkout.objects.filter(buyer=buyer)
            check=check[::-1]
            check=check[0]
        else:
            check = Checkout.objects.get(id=checkid)
            check.rppid=rppid
            check.paymentStatus=2
            check.save()

        subject = 'Order has been placed : Team Shopkaro'
        message = f"""Hi {buyer.name}, Your order  has been placed with order id {rppid}
                      kindly track you order in profile section 
                      Team:Shopkaro."""
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [buyer.email, ]
        send_mail( subject, message, email_from, recipient_list )
        return HttpResponseRedirect("/confirmation/")
 


@login_required(login_url="/loginpage/")    
def payAgain(request,checkid):
    try:
       buyer = Buyer.objects.get(username = request.user)
       check = Checkout.objects.get(id= checkid)
       orderAmount = check.final*100
       orderCurrency = "INR"
       paymentOrder = client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))
       paymentId=paymentOrder["id"]
       check.paymentMode = 2
       check.save()      
       return render(request,"pay.html",{
           "amount":orderAmount,
           "api_key":RAZORPAY_API_KEY,
           "order_id":paymentId,
           "User":buyer,
           "checkid":checkid
               })    
    except:
        return HttpResponseRedirect("profile")


@login_required(login_url="/loginpage/")    
def confirmationpage(request):
     return render(request,"confirmation.html")


@login_required(login_url="/loginpage/")    
def supportForm(request):
    if (request.method=="POST"):
        s=Support_Querry()
        s.username = request.POST.get("username")
        s.email = request.POST.get("email")
        s.phone = request.POST.get("phone")
        s.subject = request.POST.get("subject")
        s.message = request.POST.get("message")
        s.save()
        messages.success(request, "Your Querry has been submitted !!!. Our team will contact you soon. Thank you!!!")
    return render(request,"support.html")




def forgetPassword1(request):
    if(request.method=="POST"):
        username = request.POST.get("username")
        try:
          user = Buyer.objects.get(username=username)
          otp = randint(100000,999999)
          user.otp = otp
          user.save()
          request.session["reset-password-username"] = username

          subject = 'Otp for reset password : Team Shopkaro'
          message = f"""Hi {user.username}, your One time password(OTP) is {otp}
                        Never share OTP with anyone 
                        Team:Shopkaro."""
          email_from = settings.EMAIL_HOST_USER
          recipient_list = [user.email, ]
          send_mail( subject, message, email_from, recipient_list )
          return HttpResponseRedirect("/forgetPassword2/")
        


        except:
            messages.error(request,"Invalid Username")  
    return render(request,"forgetPassword1.html") 


def forgetPassword2(request):
    if(request.method=="POST"):
        otp = request.POST.get("otp")
        
        try:
            user  = Buyer.objects.get(username = request.session.get("reset-password-username"))
            

            if (int(otp)==user.otp):
               

                return HttpResponseRedirect("/forgetPassword3/")
            else: 
                  messages.error( request,"Error!! Invalid otp!!!") 
            
    
        except:
            messages.error(request,"Un-Authorized")
 
    return render(request,"forgetPassword2.html")



def forgetPassword3(request):
    if(request.method=="POST"):
       password=  request.POST.get("password")
       cpassword=  request.POST.get("cpassword")
       if(password==cpassword):
            try:
                print("one")

                user  = User.objects.get(username = request.session.get("reset-password-username"))
                user.set_password(password)
                user.save()
                if(request.session["reset-password-username"]):
                    del request.session["reset-password-username"]

                return HttpResponseRedirect("/loginpage")
            except:
                 messages.error(request,"Un-Authorized")
       else:
           messages.error(request," OOPS!!! Password does not matched")
     
    return render(request,"forgetPassword3.html")
