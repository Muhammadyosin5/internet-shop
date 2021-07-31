from django.shortcuts import render, redirect
from .models import *
from cart.cart import Cart
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def homepage(request):
    products = Product.objects.all()
    categoryes = Category.objects.all()

    if request.method == "POST" and request.POST.get('category_id'):
        products = Product.objects.filter(category=request.POST.get('category_id'))
    elif request.method == "GET" and request.POST.get('all_products'):
        products = Product.objects.all()
    else:
        products = Product.objects.all()

    context1 = {
        'categoryes' : categoryes,
        'products':products
    }
    return render(request, 'eshopapp/index.html', context1)

# Views for customer cart

@login_required(login_url="login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("homepage")


@login_required(login_url="login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_detail(request):
    return render(request, 'eshopapp/cart.html')



def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')

    context = {'form':form}
    return render(request, 'eshopapp/index.html', context)

def registration(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        form = CreateUserForm
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'akkaunt muvofaqiyatli yaratildi' + user + 'uchun')

                return redirect('login')

        context = {'form':form}
        return render(request, 'eshopapp/register.html', context)

def login_page(request):
	if request.user.is_authenticated:
		return redirect('homepage')
	else:
		if request.method == "POST":
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('homepage')
			else:
				messages.info(request, 'username or password is incorrect')

		context = {}
		return render(request, 'eshopapp/register.html', context)

def logout_user(request):
	logout(request)
	return redirect('login')
