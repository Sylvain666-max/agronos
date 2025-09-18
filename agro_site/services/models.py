from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Service(models.Model):
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=240, blank=True)
    price_from = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)  

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('services:service_detail', args=[self.slug])

class QuoteRequest(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='quotes')
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Devis {self.name} - {self.service.name}"
    
from django.db import models

class Purchase(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    stripe_session_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    customer_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.title} - {self.customer_email}"

# services/models.py
from django.db import models
from django.utils.text import slugify

class ProductCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Product Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
