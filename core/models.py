from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="FontAwesome class e.g. fa-solid fa-sun")

    def __str__(self):
        return self.name


class Feature(models.Model):
    text = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="FontAwesome class e.g. fa-solid fa-truck-fast")

    def __str__(self):
        return self.text


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to="products/")
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

from django.db import models

class Lead(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.product.name}"
