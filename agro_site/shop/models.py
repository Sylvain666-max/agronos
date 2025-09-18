from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12,decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True) 
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])

ORDER_STATUS = (
    ('pending', 'En attente'),
    ('confirmed', 'Confirmée'),
    ('shipped', 'Expédiée'),
    ('completed', 'Terminée'),
    ('cancelled', 'Annulée'),
)

PAYMENT_METHODS = (
    ('momo', 'Mobile Money'),
    ('card', 'Carte Bancaire'),
    ('cod', 'Paiement à la livraison'),
)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=120, blank=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='cod')
    status = models.CharField(max_length=12, choices=ORDER_STATUS)
    notes = models.TextField(blank=True)
    paid=models.BooleanField(default=False)
        


    def __str__(self):
        return f"Commande #{self.id} - {self.full_name}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())    

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=12,decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_cost(self):
        return self.price * self.quantity    
