from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   
    path('',views.home,name='home'),
    path("place_order/", views.place_order, name="place_order"),   # for form submission
    path("leads/", views.leads_page, name="leads_page"),           # for viewing leads
    path("search/", views.search, name="search"),
    path("search-suggestions/", views.search_suggestions, name="search_suggestions"),





]