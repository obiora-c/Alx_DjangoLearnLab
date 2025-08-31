from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    description =models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    stock_quantity = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)    
    
    
    class Meta:
          ordering = ["-created_date"]
          indexes = [models.Index(fields=["name"])]


    def __str__(self):
     return self.name
 
    def reduce_stock(self, qty: int):
        if qty <= 0:
            return
        if qty > self.stock_quantity:
            raise ValueError("Not enough stock")
        self.stock_quantity -= qty
        self.save(update_fields=['stock_quantity'])