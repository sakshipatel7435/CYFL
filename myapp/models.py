from django.db import models
from django.utils.safestring import mark_safe


# Create your models here.
class registermodel(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.firstname
    
class category(models.Model):
    catname = models.CharField(max_length=20)
    def __str__(self):
        return self.catname


class Type(models.Model):
    typename = models.CharField(max_length=30)

    def __str__(self):
        return self.typename




class product(models.Model):
    name=models.CharField(max_length=20)
    pimage=models.ImageField(upload_to="photos")
    catid=models.ForeignKey(category,on_delete=models.CASCADE)
    typeid=models.ForeignKey(Type,on_delete=models.CASCADE,null=True)
    price=models.FloatField()
    description= models.TextField()
    # size=models.CharField(max_length=4)
    # color=models.CharField(max_length=10)
    status= models.CharField(max_length=20)

    def product_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.pimage.url))

    product_photo.allow_tags = True

    def __str__(self):
        return self.name

class productimages(models.Model):
    pid = models.ForeignKey(product,on_delete=models.CASCADE)
    pimage = models.ImageField(upload_to="photos")

    def product_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.pimage.url))

    product_photo.allow_tags = True


class cart(models.Model):
    userid=models.ForeignKey(registermodel,on_delete=models.CASCADE)
    productid = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    totalamount=models.FloatField()
    orderstatus=models.IntegerField(default=1)
    orderid=models.IntegerField(default=0)


class wishlist(models.Model):
    userid=models.ForeignKey(registermodel,on_delete=models.CASCADE)
    productid = models.ForeignKey(product, on_delete=models.CASCADE)
    stockstatus = models.CharField(max_length=100, null=True, blank=True)
    # stock=models.CharField(max_length=20)


class ordermodel(models.Model):
   userid = models.ForeignKey(registermodel, on_delete=models.CASCADE)
   finaltotal = models.FloatField()
   phone = models.BigIntegerField()
   address = models.TextField()
   paymode = models.CharField(max_length=40)
   timestamp = models.DateTimeField(auto_now_add=True)
   status = models.BooleanField(default=False)
   razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)















