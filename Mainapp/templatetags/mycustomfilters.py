from django import template

register = template.Library()


@register.filter(name="paymentModefilter")
def paymentModefilter(request, status):
    if (status == 1):
         return "COD"
    else:
         return "Net Banking / UPI"     


@register.filter(name="paymentStatusfilter")
def paymentStatusfilter(request, status):
    if (status == 1):
         return "Pending"
    else:
         return "Paid" 
    

@register.filter(name="orderStatusfilter")
def orderStatusfilter(request, status):
    if (status == 1):
         return "Order Placed"
    elif(status==2):
         return "Ready to Dispatch"    
    elif(status==3):
         return "Dispatched"    
    elif(status==4):
         return "Out for delivery"    
    elif(status==5):
         return "Delivered"    
    


@register.filter(name="checkForRepayment")
def checkForRepayment(request, checkout):
    if (checkout.paymentStatus==1 and checkout.paymentMode == 2):
         return True
    else:
         return  False
    