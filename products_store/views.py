from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect


from .models import Product, Supplier


@login_required(login_url='/login/')
def home(request):
    return render(request, 'products_store/home.html')



@login_required
def supplier_dashboard(request):
    if not request.user.groups.filter(name='Supplier').exists():
        return redirect('home')
    supplier = Supplier.objects.get(user=request.user)
    products = Product.objects.filter(supplier=supplier)
    cheaper_analogues = []
    for product in products:
        cheaper = Product.objects.filter(product_code=product.product_code,
                                         price__lt=product.price).exclude(
            supplier=supplier)
        if cheaper.exists():
            cheaper_analogues.append(cheaper.get())
    return render(request, 'products_store/supplier_dashboard.html',
                  {'products': products, 'cheaper_analogues': cheaper_analogues})


@login_required
def buyer_dashboard(request):
    IN_STOCK = 'In stock'
    if not request.user.groups.filter(name='Buyer').exists():
        return redirect('home')
    products = Product.objects.filter(stock_status=IN_STOCK)
    return render(request, 'products_store/buyer_dashboard.html', {'products': products})


class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        if user.is_superuser or user.groups.filter(name='Administrator').exists():
            return redirect('/admin')
        elif user.groups.filter(name='Supplier').exists():
            return redirect('supplier_dashboard')
        elif user.groups.filter(name='Buyer').exists():
            return redirect('buyer_dashboard')
        else:
            return redirect('home')
