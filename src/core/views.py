from typing import List
from django import template
from django.db import models
from django.forms.widgets import CheckboxInput
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, render
from .models import Item, OrderItem, Order, BillingAddress, Banner, Home, HomeAboutNote, About, Contact
from django.views.generic import ListView, DetailView, View
from django.utils import timezone

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm
# Create your views here.

def item_list(request):
    context = {
        'items' : Item.objects.all()
    }
    return render(request, "home-page.html", context)

class CheckoutView(View):
    def get(self, *args, **kwargs):
        print(self.request.POST)
        item = Item.objects.filter(slug = kwargs['slug'])[0]
        form = CheckoutForm()
        context = {
            'item': item,
            'form': form,
        }
        return render(self.request, 'checkout-page.html', context)
    
    def post(self, *args, **kwargs):
        print('inside the post')
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user = self.request.user, ordered = False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                same_billing_address = form.cleaned_data.get('same_billing_address')
                save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')

                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address= street_address,
                    apartment_address = apartment_address,
                    country = country,
                    zip = zip,
                    # same_billing_address,
                    # save_info,
                    # payment_option,

                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # TODO: add redirect to payment option
                return redirect("core:payment")
            messages.warning(self.request, "Failed Checkout")
            return redirect("core:checkout")
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have any active order.")
            return redirect("core:order-summary")

        

class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "payment.html")
def product(request):
    context = {}
    return render(request, "product-page.html", context)

class HomeView(View):
    def get(self, *args, **kwargs):
        featured_products = Item.objects.filter(featured = True)
        home = Home.objects.all()[0]
        notes = home.notes.all()
        context ={
            'banner':home.banner,
            'title':home.about_title,
            'small_title' : home.small_title,
            'image' : home.about_image,
            'notes':notes,
            'purchase_now_title':home.purchase_now_title,
            'purchase_now_description':home.purchase_now_description,
        }
        if featured_products.exists():
            context['object_list'] = featured_products
            return render(self.request, 'index.html', context)
        else:
            return render(self.request, 'index.html', context)


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'
def add_order(request, order_item, order_qs, item):
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart")
            return redirect("core:product", slug = slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item quantity was updated.")
        return redirect("core:order-summary")

# @login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug = slug)
    try:
        order_item, created = OrderItem.objects.get_or_create(item = item, user = request.user, ordered = False)
        order_qs = Order.objects.filter(user = request.user, ordered = False)
        add_order(request, order_item,order_qs,item)
        # if order_qs.exists():
        #     order = order_qs[0]
        #     if order.items.filter(item__slug = item.slug).exists():
        #         order_item.quantity += 1
        #         order_item.save()
        #         messages.info(request, "This item quantity was updated.")
        #         return redirect("core:order-summary")
        #     else:
        #         order.items.add(order_item)
        #         messages.info(request, "This item was added to your cart")
        #         return redirect("core:product", slug = slug)
        # else:
        #     ordered_date = timezone.now()
        #     order = Order.objects.create(user = request.user, ordered_date = ordered_date)
        #     order.items.add(order_item)
        #     messages.info(request, "This item quantity was updated.")
        #     return redirect("core:order-summary")
    except:
              # if we want use the cookie
        # we get the cookie using below method
        device = request.COOKIES['device']
        order_item, created = OrderItem.objects.get_or_create(item = item, device = device, ordered = False)
        order_qs = Order.objects.filter(device = device , ordered = False)
        add_order(request, order_item,order_qs,item)
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug = slug)
    order_qs = Order.objects.filter(user = request.user, ordered = False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(item = item, user = request.user, ordered = False)[0]
            order.items.remove(order_item)
            order.save()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")

        
        else:
            # order does not contain the item
            messages.info(request, "This item was not in your cart.")
            return redirect("core:product", slug = slug)
   
    else:
        # add a message that user has no order
        messages.info(request, "You do not have any active order.")
        return redirect("core:product", slug = slug)

class OrderSummaryView( LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user = self.request.user, ordered = False)
            context = {
                'object':order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have any active order.")
            return redirect("/")


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug = slug)
    order_qs = Order.objects.filter(user = request.user, ordered = False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(item = item, user = request.user, ordered = False)[0]

            if order_item.quantity >1:
                order_item.quantity -=1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item qunatity was updated.")
            return redirect("core:order-summary")

        
        else:
            # order does not contain the item
            messages.info(request, "This item was not in your cart.")
            return redirect("core:product", slug = slug)
   
    else:
        # add a message that user has no order
        messages.info(request, "You do not have any active order.")
        return redirect("core:product", slug = slug)

class MyProductsView(ListView):
    model = Item
    paginate_by = 10
    template = 'products.html'

class AboutView(View):
    def get(self, *args, **kwargs):
        about_data = About.objects.filter(selected = True)
        if about_data.exists():
            about_data= about_data[0]
            old_works = Item.objects.filter(sold = True)
            if old_works.exists():
                old_works = old_works.all()
            else:
                old_works= None
            context = {
                'data':about_data,
                'old_works': old_works
            }
            return render(self.request, 'about.html',context)

        return render(self.request, 'about.html',{})

class ContactView(View):
    def get(self, *args, **kwargs):
        contact_data = Contact.objects.filter(selected = True)
        if contact_data.exists():
            contact_data= contact_data[0]
            context = {
                'data':contact_data,
            }
            return render(self.request, 'contact.html',context)

        return render(self.request, 'contact.html',{})
