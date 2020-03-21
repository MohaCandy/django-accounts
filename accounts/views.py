from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .forms import OrderForm

from .models import Customer, Order, Product, Tag
from .filters import OrderFilter, CustomerFilter
# Create your views here.

def loginPage(request):

    return render(request, 'accounts/login.html')

def registerPage(request):

    return render(request, 'accounts/register.html')

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

def product(request):
    products = Product.objects.all()
    return render(request, 'accounts/product.html', {'products': products})

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


def deleteOrder(request, pk):

    order = Order.objects.get(id = pk)
    # form = OrderForm(instance=order)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete.html', context)