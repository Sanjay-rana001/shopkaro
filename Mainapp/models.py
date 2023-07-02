from django.db import models


# Create your models here.
class Maincategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
          return self.name

class Subcategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    def __str__(self):
          return self.name

class Brands(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    pic2 = models.ImageField(upload_to="Product",default="",blank=True,null=True)

    def __str__(self):
          return self.name

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    maincategory = models.ForeignKey(Maincategory,on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    brands = models.ForeignKey(Brands,on_delete=models.CASCADE)
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=30)
    base_price = models.IntegerField()
    discount = models.IntegerField()
    final_price = models.IntegerField()
    description = models.TextField(default="",null=True,blank=True)
    pic1 = models.ImageField(upload_to="Product",)
    pic2 = models.ImageField(upload_to="Product",default="",blank=True,null=True)
    pic3 = models.ImageField(upload_to="Product",default="",blank=True,null=True)
    pic4 = models.ImageField(upload_to="Product",default="",blank=True,null=True)
    stock = models.BooleanField(default=True)
    def __str__(self):
          return str(self.id)+" / "+ self.name
     

class Buyer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,default="",blank=True,null=True)
    username = models.CharField(max_length=30,default="",blank=True,null=True)
    email = models.EmailField(max_length=50,default="",blank=True,null=True)
    phone = models.CharField(max_length=15,default="",blank=True,null=True)
    addressline1 = models.CharField(max_length=100,default="None",blank=True,null=True)
    addressline2 = models.CharField(max_length=100,default="None",blank=True,null=True)
    addressline3 = models.CharField(max_length=100,default="None",blank=True,null=True)
    pin = models.CharField(max_length=30,default="None",blank=True,null=True)
    city = models.CharField(max_length=30,default="None",blank=True,null=True)
    state = models.CharField(max_length=30,default="None",blank=True,null=True)
    pic = models.ImageField(upload_to="buyers" ,default="",blank=True,null=True)
    otp = models.IntegerField(default=888888)
    

    def __str__(self):
          return  str(self.id)+" / "+ self.name
     
          
class Wishlist(models.Model):
     id = models.AutoField(primary_key=True)
     buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
     product = models.ForeignKey(Product, on_delete=models.CASCADE)

     def __str__(self):
          return str(self.id) +"/"+ self.buyer.username
     




paymentMode = ((1,"COD"),(2,"Net Banking"))
paymentStatus = ((1,"pending"),(2,"Paid"))
orderStatus = ((1,"Order Placed"),(2,"Ready to Dispatch"),(3,"Dispatched"),(4,"Out for delovery"),(5,"Delivered"))
class Checkout(models.Model):
     id = models.AutoField(primary_key=True)     
     buyer = models.ForeignKey(Buyer,on_delete= models.CASCADE)
     paymentMode = models.IntegerField(choices=paymentMode,default=1)
     paymentStatus = models.IntegerField(choices=paymentStatus,default=1)
     orderStatus = models.IntegerField(choices=orderStatus,default=1)
     subtotal = models.IntegerField(default=0)
     shipping = models.IntegerField()
     final = models.IntegerField()
     rppid = models.CharField(max_length=30,default="")
     date = models.DateTimeField(auto_now=True)

     def __str__(self):
          return str(self.id) +"/"+ self.buyer.username
     




class CheckoutProducts(models.Model):
     id = models.AutoField(primary_key=True)  
     checkout = models.ForeignKey(Checkout,on_delete=models.CASCADE)   
     product = models.ForeignKey(Product,on_delete=models.CASCADE)
     qty = models.IntegerField(default=0)
     total = models.IntegerField(default=0)
     
     def __str__(self):
         return str(self.id) +"/"+str(self.checkout.id) +"/"+ self.product.name


supportStatus= ((1,"Active"),(2,"Resolved"))
class Support_Querry(models.Model):
    id = models.AutoField(primary_key=True) 
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15) 
    subject = models.CharField(max_length=50)
    message  = models.TextField(max_length=200)
    status = models.IntegerField(choices=supportStatus,default=1)
    date = models.DateTimeField(auto_now=True)


    def __str__(self):
         return str(self.id)+"/"+self.username+"/"+self.subject
         


