from django.contrib import admin

# Register your models here.
from .models import (Item, OrderItem, Order, ImageItem, Banner,
 HomeAboutNote, Home, About, Contact)

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(ImageItem)
admin.site.register(Banner)
admin.site.register(HomeAboutNote)
admin.site.register(Home)
admin.site.register(Contact)
admin.site.register(About)