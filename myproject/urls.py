"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from myapp import views
from myproject import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.indexpage),
    path('index-2',views.indexpage),
    path('about',views.aboutpage),
    path('contact',views.contactpage),
    # path('login-register',views.loginregisterpage),
    path('register',views.registerpage),
    path('login',views.loginpage),
    path('my-account',views.myaccountpage),
    # path('checkout', views.checkout),
    path('cart',views.showcart),
    path('wishlist',views.showwishlist),
    path('fetchlogindata', views.fetchlogindata),
    path('fetchregisterdata', views.fetchregisterdata),
    path("logout",views.logout),
    path("shop-left-sidebar",views.shopleftsidebar),
    path('single-product/<int:id>', views.singleproductpage),
    path("insertintocart", views.insertintocart),
    path("insertintowishlist", views.insertintowishlist),
    path('placeorder', views.placeorder),
    path('userorder', views.orderhistory),
    path('payment-success', views.payment_success),
    path("deleteitem/<int:id>", views.deleteitem),
    path("increase/<int:id>", views.increase),
    path("decrease/<int:id>", views.decrease),
    path("yourorderdetails/<int:id>",views.yourorderdetails),
    path("mencat/<int:id>",views.mencat),
    path("womencat/<int:id>",views.womencat),
    path("kidcat/<int:id>",views.kidcat),
    path("removewish/<int:id>",views.removewish),
    path("forgot",views.forgot),
    path("forgotpassword",views.forgotpassword),
    path("cancelorder/<int:id>", views.cancelorder),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
