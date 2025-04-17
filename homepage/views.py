from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from customers import views
from .forms import UserCreateForm
from customers.models import *
# from customers.forms import  CustomerForm




def index(request):
    page = 'login'

    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('loggedin')
            else:
                messages.error(request, 'Invalid password')
        except User.DoesNotExist:
            messages.error(request, 'Username does not exist')

    context = {'page':page}
    return render(request, "homepage/index.html", context)

def loggedIn(request):
    return render(request,"homepage/loggedin.html")

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('loggedin')

# user = Customer.objects.get(id =pk)
# print(user)

# def feedback(request):
    
#     user = request.user.id
#     required_user = Customer.objects.get(id = user)
#     print(required_user)
#     # form = CustomerFeedbackForm(instance=required_user)
#     # if request.method == 'POST':
#     #     form = CustomerFeedbackForm(request.POST, instance=required_user)
#     #     if form.is_valid():
#     #         form.save()
#     #         messages.success(request, "Your feedback sent successfully. Thank you.")
#     # context = {'form':form}
#     return render(request,"homepage/feedback.html")

def registerUser(request):
    page = 'register'
    form = UserCreateForm()

    if request.method=="POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('loggedin')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            for error in form.non_field_errors():
                messages.error(request, error)

    context={'page':page, 'form':form}
    return render(request, 'homepage/index.html', context)