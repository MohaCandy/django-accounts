from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .forms import OrderForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Customer, Order, Product, Tag
from .filters import OrderFilter, CustomerFilter

from django.contrib import messages
# Create your views here.

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password wrong!!')
        context = {}
        return render(request, 'accounts/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')


def registerPage(request):

    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'User (' + user + ') is succesfully registered')
                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)

@login_required(login_url='login')
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    customerFilter = CustomerFilter(request.GET, queryset=customers)
    customers = customerFilter.qs

    total_orders = orders.count()
    delivered_order = orders.filter(status="Delivered").count()
    pending_order = orders.filter(status="Pending").count()

    context = {'customers':customers, 'orders':orders, 'total_orders':total_orders,
     'delivered_order':delivered_order, 'pending_order':pending_order, 'customerFilter': customerFilter}
    return render(request, 'accounts/dashboard.html', context,)


@login_required(login_url='login')
def product(request):
    products = Product.objects.all()
    return render(request, 'accounts/product.html', {'products': products})


@login_required(login_url='login')
def customer(request, index):
    customer = Customer.objects.get(id=index)
    orders = customer.order_set.all()
    email = customer.email
    phone = customer.phone
    FilterForm = OrderFilter(request.GET, queryset=orders)
    
    orders = FilterForm.qs
    total_orders = orders.count()

    context = {'customer': customer, 'orders': orders,
                'email': email, 'phone': phone,
                'total_orders': total_orders,
                'FilterForm': FilterForm}

    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
def createOrder(request, index):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=2)
    customer = Customer.objects.get(id=index)
    # form = OrderForm(initial={'customer': customer})
    formSet = OrderFormSet(queryset= Order.objects.none(), instance=customer)
    if request.method == "POST":
        newIntry = OrderFormSet(request.POST, instance=customer)
        if newIntry.is_valid():
            newIntry.save()
            return redirect('/')


    context = {'formSet': formSet}

    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def updateOrder(request, pk):

    order = Order.objects.get(id = pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        updatedItem = OrderForm(request.POST, instance=order)
        if updatedItem.is_valid():
            updatedItem.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def deleteOrder(request, pk):

    order = Order.objects.get(id = pk)
    # form = OrderForm(instance=order)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete.html', context)