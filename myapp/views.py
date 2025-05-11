from django.shortcuts import render, redirect
from myapp.models import *
from django.contrib import messages
import razorpay
from django.conf import settings
# Create your views here.


def indexpage(request):
    categories = category.objects.all()
    products = product.objects.all()[:4]
    context = {
        'categories': categories,
        'products':products
    }
    return render(request,"index.html",context)

def registerpage(request):
    return render(request,"register.html")

def loginpage(request):
    return render(request,"login.html")

def contactpage(request):
    categories = category.objects.all()
    context = {
        "categories": categories
    }
    return render(request,"contact.html",context)

def aboutpage(request):
    categories = category.objects.all()
    context = {
        "categories": categories
    }
    return render(request,"about.html",context)
def myaccountpage(request):
    return render(request,"my-account.html")

# def checkout(request):
#     return render(request,"checkout.html")


def shopleftsidebar(request):
    # query to fetch all category data
    # select * from category
    fetchproducts = product.objects.all()
    context = {
        "products": fetchproducts
    }
    return render(request,"shop-left-sidebar.html",context)

def mencat(request,id):
    categories = category.objects.all()
    fetchproducts = product.objects.filter(catid=id,typeid=2)
    context = {
        "categories":categories,
        "products": fetchproducts
    }
    return render(request,"shop-left-sidebar.html",context)

def womencat(request,id):
    categories = category.objects.all()
    fetchproducts = product.objects.filter(catid=id,typeid=1)
    context = {
        "categories": categories,
        "products": fetchproducts
    }
    return render(request,"shop-left-sidebar.html",context)

def kidcat(request,id):
    categories = category.objects.all()
    fetchproducts = product.objects.filter(catid=id,typeid=3)
    context = {
        "categories": categories,
        "products": fetchproducts
    }
    return render(request,"shop-left-sidebar.html",context)


def insertproductdata(request):
    name = request.POST.get("pname")
    catid = request.POST.get("pcat")
    price = request.POST.get("pprice")
    desc = request.POST.get("pdesc")
    status = request.POST.get("pstatus")
    image = request.FILES["pimage"]

#     #seller id
#     sellerid=request.session["log_id"]
#
    insertquery = product(name=name,catid=category(id=catid),price=price,pimage=image,description=desc,status=status)
    insertquery.save()
    messages.success(request,"product added successfully")
    return render(request,"index.html")

def singleproductpage(request,id):
    print(id)
    # select * from products where id=id
    fetchdata = product.objects.get(id=id)  # will send single row as output
    prodimages = productimages.objects.filter(pid=id)
    context = {
        "data": fetchdata,
        "images":prodimages
    }
    return render(request,"single-product.html",context)

def fetchregisterdata(request):
    firstname = request.POST.get("firstname")
    lastname = request.POST.get("lastname")
    email = request.POST.get("email")
    password = request.POST.get("password")
    # print(firstname)
    # print(lastname)
    # print(email)
    # print(password)
    # Query to store data into model
    insertquery = registermodel(firstname=firstname, lastname=lastname,email=email, password=password)
    insertquery.save()
    print("success")

    return render(request,"index.html")

    # login
def fetchlogindata(request):
    uemail = request.POST.get("email")
    upassword = request.POST.get("password")

    print(uemail)
    print(upassword)

    try:
        userdata = registermodel.objects.get(email=uemail, password=upassword)
        print(userdata)

        # start session
        request.session["log_id"] = userdata.id
        request.session["log_firstname"] = userdata.firstname
        request.session["log_email"] = userdata.email

        print("session name", request.session["log_firstname"])

    except:
        print("failure")
        userdata = None

    if userdata is not None:
        return redirect("/")
    else:
        print("invalid email or password")
        messages.error(request, "invalid email or password")
        return redirect("/")
    return render(request, "login.html")

def logout(request):
    try:
        del request.session["log_id"]
        del request.session["log_firstname"]
        del request.session["log_email"]
    except:
        pass

    return render(request, "index.html")


def insertintocart(request):
    userid = request.session["log_id"]
    pid = request.POST.get("pid")
    price = request.POST.get("price")
    quantity = request.POST.get("quantity")
    totalamount = int(quantity) * float(price)

    insertquery = cart(userid=registermodel(id=userid),productid=product(id=pid),
                       quantity=quantity,totalamount=totalamount,orderid=0,orderstatus=1)
    insertquery.save()
    messages.success(request,"Product Added to Cart")
    return redirect("/")

def showcart(request):
    userid__loggedin = request.session["log_id"]
    fetchdata = cart.objects.filter(userid=userid__loggedin,orderstatus=1)
    total = sum(item.totalamount for item in fetchdata)

    context = {
        "data":fetchdata,
        "total":total
    }
    return render(request,"cart.html",context)

def deleteitem(request,id):
    print(id)
    # delete from cart where id=id
    cart.objects.get(id=id).delete()
    messages.success(request,"Item Removed")
    return redirect(showcart)


def increase(request,id):
    try:
        fetchdata = cart.objects.get(id=id)
        fetchdata.quantity += 1
        fetchdata.totalamount += fetchdata.productid.price
        messages.success(request,"Increased")
        fetchdata.save()
        return redirect(showcart)
    except Exception as e:
        print(e)

def decrease(request,id):
    fetchdata = cart.objects.get(id=id)

    if fetchdata.quantity == 1:
        fetchdata.delete()
    else:
        fetchdata.quantity -= 1
        fetchdata.totalamount -= fetchdata.productid.price
        fetchdata.save()
    return redirect(showcart)

def placeorder(request):
    userid = request.session["log_id"]
    finaltotal = request.POST.get("total")
    phone = request.POST.get("phone")
    address = request.POST.get("address")
    payment = request.POST.get("payment")

    print("userid: ",userid,"finaltotal: ",finaltotal,"phone: ",phone,"address: ",address,"payment: ",payment)

    if payment=="Cash on Delivery":
        storedata = ordermodel(userid=registermodel(id=userid),finaltotal=finaltotal,phone=phone,
                               address=address,paymode=payment,status=True)
        storedata.save()
        print("Order Placed")

        lastid = storedata.id
        # update status in cart model
        fetchdata = cart.objects.filter(userid=userid, orderstatus=1)

        for i in fetchdata:
            i.orderstatus = 0
            i.orderid = lastid
            i.save()

        print("Status updated in Cart")

        return redirect("/")
    else:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
        order_amount = int(float(finaltotal) * 100)  # Razorpay needs amount in paise
        razorpay_order = client.order.create({
            "amount": order_amount,
            "currency": "INR",
            "receipt": f"order_rcptid_{userid}",
            "payment_capture": "1",
        })

        storedata = ordermodel(
            userid=registermodel(id=userid),
            finaltotal=finaltotal,
            phone=phone,
            address=address,
            paymode="Online",
            status = True,
            razorpay_order_id=razorpay_order['id'],
        )
        storedata.save()

        lastid = storedata.id

        # Update Cart Items
        cart_items = cart.objects.filter(userid=userid, orderstatus=1)
        for item in cart_items:
            item.orderstatus = 0
            item.orderid = lastid
            item.save()

        return render(request, "payment.html", {
            "razorpay_order_id": razorpay_order['id'],
            "amount": order_amount,
            "key": settings.RAZORPAY_KEY_ID,
            "currency": "INR",
        })

    return redirect("/")


def orderhistory(request):
    userid = request.session["log_id"]
    myorders = ordermodel.objects.filter(userid=userid)
    context = {
        'data':myorders
    }
    return render(request,'order.html',context)




def cancelorder(request, id):
    myorders = ordermodel.objects.get(id=id)
    myorders.status = False
    myorders.save()
    messages.success(request,"Your Order Has Been Canceled Successfully.")
    return redirect(orderhistory)


def payment_success(request):
  return render(request, "index.html")


def insertintowishlist(request):
    pid = request.POST.get("pid")
    price = request.POST.get("pprice")
    userid = request.session["log_id"]
    stockstatus = request.POST.get('stockstatus', 'In Stock')
    # stock = request.POST.get("stock")
    # totalamount = float(price) * int(quantity)


    insertquery = wishlist(userid=registermodel(id=userid),productid=product(id=pid),stockstatus=stockstatus)
    insertquery.save()
    messages.success(request, "item added successfully to wishlist")
    return redirect("/")

def showwishlist(request):
    userid = request.session["log_id"]
    fetchdata = wishlist.objects.filter(userid=userid)
    context = {
        "data":fetchdata
    }
    return render(request,"wishlist.html",context)



# def checkout(request):
#     firstname = request.POST.get("firstname")
#     lastname = request.POST.get("lastname")
#     Address = request.POST.get("address")
#     city = request.POST.get("city")
#     state= request.POST.get("state")
#     postcode= request.POST.get("postcode")
#     emailaddress= request.POST.get("emailaddress")
#     phone= request.POST.get("phone")
#
#     print(firstname),
#     print(lastname),
#     print(Address),
#     print(city),
#     print(state),
#     print(postcode),
#     print(emailaddress),
#     print(phone)
#
#     return render(request,"checkout.html")


def yourorderdetails(request,id):
    fetchdata = cart.objects.filter(orderid=id)
    context = {
        "data":fetchdata
    }
    return render(request,"singleorder.html",context)

def removewish(request,id):
    wishlist.objects.get(id=id).delete()
    messages.success(request, "Item Removed")
    return redirect("/wishlist")

def forgot(request):
    return render(request,"forgot.html")

def forgotpassword(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        try:
            user = registermodel.objects.get(email=username)

        except registermodel.DoesNotExist:
            user = None
        # if user exist then only below condition will run otherwise it will give error as described in else condition.
        if user is not None:
            #################### Password Generation ##########################
            import random

            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                       'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

            nr_letters = 6
            nr_symbols = 1
            nr_numbers = 3
            password_list = []

            for char in range(1, nr_letters + 1):
                password_list.append(random.choice(letters))

            for char in range(1, nr_symbols + 1):
                password_list += random.choice(symbols)

            for char in range(1, nr_numbers + 1):
                password_list += random.choice(numbers)

            print(password_list)
            random.shuffle(password_list)
            print(password_list)

            password = ""  # we will get final password in this var.
            for char in password_list:
                password += char

            ##############################################################

            msg = "hello here it is your new password  " + password  # this variable will be passed as message in mail

            ############ code for sending mail ########################

            from django.core.mail import send_mail

            send_mail(
                'Your New Password',
                msg,
                'parthinfolabz19@gmail.com',
                [username],
                fail_silently=False,
            )
            # NOTE: must include below details in settings.py
            # detail tutorial - https://www.geeksforgeeks.org/setup-sending-email-in-django-project/
            # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
            # EMAIL_HOST = 'smtp.gmail.com'
            # EMAIL_USE_TLS = True
            # EMAIL_PORT = 587
            # EMAIL_HOST_USER = 'mail from which email will be sent'
            # EMAIL_HOST_PASSWORD = 'pjobvjckluqrtpkl'   #turn on 2 step verification and then generate app password which will be 16 digit code and past it here

            #############################################

            # now update the password in model
            cuser = registermodel.objects.get(email=username)
            cuser.password = password
            cuser.save(update_fields=['password'])

            print('Mail sent')
            messages.info(request, 'mail is sent')
            return redirect("/")

        else:
            messages.info(request, 'This account does not exist')
        return redirect("/")











