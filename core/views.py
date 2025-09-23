from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Category, Feature, Product,Lead
from django.http import JsonResponse

def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_featured=True)[:3]
    products = Product.objects.all()
    return render(request, 'index.html', {
        "categories": categories,
        "products": products,
        "featured_products": featured_products,
    })

def place_order(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        notes = request.POST.get("notes")
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        # ✅ Save to database as a Lead
        Lead.objects.create(
            product=product,
            name=name,
            phone=phone,
            address=address,
            notes=notes
        )

        messages.success(request, "Your order has been placed successfully!")
        return redirect("home")

    return redirect("home")

from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def leads_page(request):
    leads = Lead.objects.all().order_by("-created_at")
    return render(request, "leads.html", {"leads": leads})




def search(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"status": "error", "message": "No search term provided."})

    # First check if query matches a category
    category = Category.objects.filter(name__icontains=query).first()
    if category:
        return JsonResponse({"status": "category", "category_id": category.id})

    # Then check if query matches a product
    product = Product.objects.filter(name__icontains=query).first()
    if product:
        return JsonResponse({
            "status": "product",
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": str(product.price),
            "image": product.image.url
        })

    # Not found
    return JsonResponse({"status": "not_found", "message": "No matching product or category found."})

from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Category

def search_suggestions(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        # Search in products
        products = Product.objects.filter(name__icontains=query)[:5]
        for p in products:
            results.append({
                "type": "product",
                "id": p.id,
                "name": p.name,
                "image": p.image.url if p.image else "",
            })

        # Search in categories
        categories = Category.objects.filter(name__icontains=query)[:5]
        for c in categories:
            results.append({
                "type": "category",
                "id": c.id,
                "name": c.name,
            })

    return JsonResponse({"results": results})
