from django.contrib import admin
from .models import *
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table,TableStyle
# Register your models here.

def export_to_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename = "report.pdf"'
    # Generate the report using ReportLab
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    # Define the style for the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    # Create the table headers
    headers = ['userid','finaltotal','phone','address','paymode','timestamp','status','razorpay_order_id']


    # Create the table data
    data = []
    for obj in queryset:
        data.append([
            obj.userid,
            obj.finaltotal,
            obj.phone,
            obj.address,
            obj.paymode,
            obj.timestamp,
            obj.status,
            obj.razorpay_order_id,
        ])

        # Create the table
    t = Table([headers] + data, style=style)
    # Add the table to the elements array
    elements.append(t)
    # Build the PDF document
    doc.build(elements)
    return response
export_to_pdf.short_description = "Export to PDF"

class showordermodel(admin.ModelAdmin):
     list_display = ['userid','finaltotal','phone','address','paymode','timestamp','status','razorpay_order_id']
     # list_filter = ['datetime']
     actions = [export_to_pdf]
admin.site.register(ordermodel,showordermodel)


class showregister(admin.ModelAdmin):
    list_display = ["id", "firstname", "lastname", "email","password"]

admin.site.register(registermodel,showregister)

class showcategory(admin.ModelAdmin):
    list_display = ["id","catname"]

admin.site.register(category,showcategory)

class showsubcategory(admin.ModelAdmin):
    list_display = ["id","typename"]

admin.site.register(Type,showsubcategory)

class showproducts(admin.ModelAdmin):
    list_display = ['id','name','price','product_photo','description','catid','typeid','status']

admin.site.register(product,showproducts)

class showcart(admin.ModelAdmin):
    list_display = ['id','userid','productid','quantity','totalamount','orderstatus','orderid']

admin.site.register(cart,showcart)

class showwishlist(admin.ModelAdmin):
    list_display = ['id','userid','productid']

admin.site.register(wishlist,showwishlist)


# class orderlist(admin.ModelAdmin):
#     list_display = ['userid','finaltotal','phone','address','paymode','timestamp','status','razorpay_order_id']
#
# admin.site.register(ordermodel,orderlist)

class showproductimages(admin.ModelAdmin):
    list_display = ["id","pid","product_photo"]

admin.site.register(productimages,showproductimages)



