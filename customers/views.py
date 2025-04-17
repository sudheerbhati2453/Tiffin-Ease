from django.http import request
from django.shortcuts import redirect, render
from .models import Customer
from .forms import CustomerForm
from django.contrib import messages
from vendorPortal.models import Vendor
from vendorPortal.views import *
from django.urls import reverse
import random


def PlanSelection(request):
    form = CustomerForm()
    
    planType = "Two Week Veg 499"
    if request.method == 'POST':
        # name_instance = Customer.objects.create(Name=request.user)
        form = CustomerForm(request.POST)
        
        if form.is_valid():
            form.save()
            # obj = Customer.objects.get(id = request.user)
            # print(obj)
            return redirect('loggedin')

    context = {'form':form}
    return render(request, "customers/planSelect.html",context)




def allotPlans(request, planType, cost):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            try:
                obj = form.save()
                Customer.objects.filter(id=obj.pk).update(Plan_Type=planType)
                messages.success(request, "Details saved successfully")
                
                vendors = Vendor.objects.all()
                allot = random.choice(vendors)
                prime_key = allot.pk
                update_cust = allot.Customers_Delivering + ", " + str(obj.pk) + " "
                Vendor.objects.filter(id=prime_key).update(Customers_Delivering=update_cust)
                
                vendor_name = allot.Vendor_Name
                vendor_phone = allot.Vendor_Phone
                messages.success(request, f"{vendor_name} is your delivery executive. Contact details: {vendor_phone}.")
                
                # Redirect to payment page instead of Free
                request.session['vendor_name'] = vendor_name
                request.session['vendor_phone'] = vendor_phone
                return redirect('payment', plan_type=planType, amount=cost)
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    
    context = {'form': form, 'cost': cost}
    return render(request, "customers/twoWeekVeg.html", context)

def Free(request):
    return allotPlans(request, "Free Trial", "Free!")

def TwoWeekVegPlan(request):
    return allotPlans(request, "Two week veg 499", "499")

def OneMonthVeg(request):
    return allotPlans(request, "One Month Veg", "799")

def OneMonthVegNonVeg(request):
    return allotPlans(request, "One Month Veg Nonveg 999", "999")

def ThreeMonthVeg(request):
    return allotPlans(request, "Three Month Veg 2499", "2499")

def ThreeMonthVegNonveg(request):
    return allotPlans(request, "Three Month Veg Non Veg", "2699")







# def TwoWeekVegPlan(request):
#     form = CustomerForm()
#     planType = "Two Week Veg 499"
#     cost = "499"
#     if request.method =='POST':
#         form = CustomerForm(request.POST)
#         if form.is_valid():
          
#             obj=form.save()
#             Customer.objects.filter(id=obj.pk).update(Plan_Type=planType)
#             messages.success(request,"Details saved successfully")
            
            
    
#     context = {'form':form, 'cost':cost}
#     return render(request,"customers/twoWeekVeg.html",context )


    


def LastPage(request):
    return render(request, 'customers/last.html')

def FreePage(request):
    return render(request,'customers/free.html')

def payment_page(request, plan_type, amount):
    context = {
        'plan_type': plan_type,
        'amount': amount,
        'vendor_name': request.session.get('vendor_name', ''),
        'vendor_phone': request.session.get('vendor_phone', '')
    }
    return render(request, 'customers/payment.html', context)

# obj = Customer.objects.all()
# # print(obj[0].pk)

# obj2 = Customer.objects.get(pk=21)
# # print(obj[0])
# # obj[1].delete()
# print(obj[0])
# obj2 = Customer.objects.update(pk=21, Plan_Type = "Veg")

# print(obj2.Full_Name)
# newObj = Customer.objects.create(Full_Name = "Arav Yadav", )