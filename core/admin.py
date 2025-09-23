from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Feature, Product,Lead

admin.site.register(Category)
admin.site.register(Feature)
admin.site.register(Product)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "product", "created_at")
    search_fields = ("name", "phone", "product__name")
    list_filter = ("created_at",)

