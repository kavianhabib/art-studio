from django.conf import settings
from django.db import models
from django.db.models.base import ModelBase, ModelStateFieldsCacheDescriptor
from django.shortcuts import reverse
from django_countries.fields import CountryField

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank = True, null = True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description =models.TextField()
    image = models.ImageField()
    image_2 = models.ImageField(null = True)
    image_3 = models.ImageField(null = True)
    image_4 = models.ImageField(null = True)
    sold = models.BooleanField(default=False)
    dimension = models.CharField(max_length=100)
    featured = models.BooleanField(default=False, null = True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs = {
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('core:add-to-cart', kwargs = {
            'slug': self.slug
        })
    def get_remove_from_cart_url(self):
        return reverse('core:remove-from-cart', kwargs = {
            'slug': self.slug
        })
class ImageItem(models.Model):
    image = models.ImageField(upload_to = 'images/')
    default = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    device = models.CharField(max_length=20, null = True)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE)

    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple = False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
        
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    device = models.CharField(max_length=20, null = True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null = True)
    ordered = models.BooleanField(default=False)

    billing_address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL, null = True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

class Banner(models.Model):
    small_title = models.CharField(max_length=100)
    big_title = models.CharField(max_length=100)
    selected = models.BooleanField(null =True, default = False)
    image_1 = models.ImageField(upload_to='images/')
    image_2 = models.ImageField(upload_to='images/', null = True)
    image_3 = models.ImageField(upload_to='images/', null = True)
    slug = models.CharField(max_length=100)

class HomeAboutNote(models.Model):
    note = models.CharField(max_length=100)
class Home(models.Model):
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE)
    about_title = models.CharField(max_length=100)
    small_title = models.CharField(max_length=100)
    about_image = models.ImageField(upload_to = 'images/')
    notes = models.ManyToManyField(HomeAboutNote)
    purchase_now_title =  models.CharField(max_length=100)
    purchase_now_description = models.CharField(max_length=100)
    selected = models.BooleanField(null = True, default=False)

    def __str__(self):
        return self.about_title

class About(models.Model):
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE)
    about_title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null = True)
    small_title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    facebook = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)
    linkedin = models.CharField(max_length=100)
    selected = models.BooleanField(null = True, default=False)

    old_works_title = models.CharField(max_length=100)
    # old_works = models.ManyToManyField(Item, null = True)

class Contact(models.Model):
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE)
    location_title = models.CharField(max_length=100)
    google_map_location = models.CharField(max_length=1000)
    about_office_title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    message_title = models.CharField(max_length=1000)
    facebook = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)
    linkedin = models.CharField(max_length=100)
    selected = models.BooleanField(null = True, default=False)




    




