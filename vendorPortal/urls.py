from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.vendorLogin, name="vendorLogin"),
    path('vendorDeliveries/',views.indexVendor, name="vendorDeliveries"),
    path('logout/', views.vendorLogout, name="vendorLogout"),
]