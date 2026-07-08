from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.views import View
from .models import Product,Customer,Cart,Wishlist,Payment
from django.db.models import Count
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'app/home.html')
def about(request):
    return render(request,'app/about.html')
def contact(request):
    return render(request,'app/contact.html')
from django.views import View
from django.shortcuts import render
from .models import Product

class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val)

        return render(request, 'app/cate.html', {
            'val': product,
            'title': title
        })
from .models import OrderPlaced

def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {
        'orders': order_placed
    })
class CategoryTitle(View):
    def get(self,request,val):
        product=Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/cate.html",{'val':product,'title':title})
class ProductDetail(View):
    def get(self,request,pk):
        product=Product.objects.get(id=pk)
        return render(request,'app/product_detail.html',{'val':product})
class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'val':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"congratulations! user Register successfully")
        else:
            messages.warning(request,"Invalid Input data")
        return render(request,'app/customerregistration.html',{'val':form})
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form})
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'congratulations! profile save successfully')
        else:
            messages.warning(request,'Invalid Input Data')


        return render(request,'app/profile.html')

def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',{'add':add})
class UpdateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        return render(request,'app/updateaddress.html',{'form':form})
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"congratulations profile updtaed successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect('address')

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)

    cart_item = Cart.objects.filter(user=user, product=product).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(user=user, product=product, quantity=1)

    return redirect('/cart')
@login_required(login_url='login')
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    shipping = 40
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + shipping
    return render(request, 'app/addtocart.html', {
        'user': user,
        'cart': cart,
        'amount': amount,
        'shipping': shipping,
        'totalamount': totalamount
    })
class checkout(View):
    def get(self, request):
        user = request.user
  
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)

        amount = 0
        shipping_amount = 40

        for p in cart_items:
            amount += p.quantity * p.product.discounted_price

        totalamount = amount + shipping_amount

        return render(request, 'app/checkout.html', {
            'add': add,
            'cart_items': cart_items,
            'totalamount': totalamount
        })

    def post(self, request):
        cust_id = request.POST.get('custid')

        if not cust_id:
            messages.warning(request, "Please select a shipping address.")
            return redirect('checkout')

        return redirect('payment')
from django.http import JsonResponse
from .models import Cart, Product

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)

        c = Cart.objects.filter(
            user=request.user,
            product=product
        ).first()

        if c:
            c.quantity += 1
            c.save()

        amount = 0

        cart_product = Cart.objects.filter(user=request.user)

        for p in cart_product:
            value = p.quantity * p.product.discounted_price
            amount += value

        totalamount = amount + 40

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }

        return JsonResponse(data)
from django.http import JsonResponse

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)

        c = Cart.objects.filter(
            user=request.user,
            product=product
        ).first()

        if c:
            if c.quantity > 1:
                c.quantity -= 1
                c.save()
            else:
                c.delete()

        amount = 0

        cart_product = Cart.objects.filter(user=request.user)

        for p in cart_product:
            value = p.quantity * p.product.discounted_price
            amount += value

        totalamount = amount + 40

        quantity = c.quantity if c else 0

        data = {
            'quantity': quantity,
            'amount': amount,
            'totalamount': totalamount
        }

        return JsonResponse(data)
from django.http import JsonResponse

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)

        Cart.objects.filter(
            user=request.user,
            product=product
        ).delete()

        amount = 0

        cart_product = Cart.objects.filter(user=request.user)

        for p in cart_product:
            value = p.quantity * p.product.discounted_price
            amount += value

        totalamount = amount + 40

        data = {
            'amount': amount,
            'totalamount': totalamount
        }

        return JsonResponse(data)
def add_to_wishlist(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)

    Wishlist(user=user, product=product).save()

    return redirect('/wishlist')
def show_wishlist(request):
    user = request.user
    wishlist = Wishlist.objects.filter(user=user)

    return render(request, 'app/wishlist.html', {
        'wishlist': wishlist
    })

def remove_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET.get("prod_id")

        wishlist_item = Wishlist.objects.filter(
            user=request.user,
            product_id=prod_id
        )

        wishlist_item.delete()

        return redirect("wishlist")
from .models import OrderPlaced

def placeorder(request):
    if request.method == "POST":

        paymentmode = request.POST.get("paymentmode")
        cust_id = request.session.get("cust_id")

        customer = Customer.objects.get(id=cust_id)

        cart = Cart.objects.filter(user=request.user)

        payment = Payment.objects.create(
            user=request.user,
            amount=0,
            paid=True if paymentmode == "Online" else False
        )

        for item in cart:
            OrderPlaced.objects.create(
                user=request.user,
                customer=customer,
                product=item.product,
                quantity=item.quantity,
                payment=payment
            )

        cart.delete()

        messages.success(request, "Order Placed Successfully")

        return redirect("orders")    
def payment(request):
    
    if request.method == "POST":

        cust_id = request.POST.get("custid")

        if not cust_id:
            messages.warning(request, "Please select an address")
            return redirect("checkout")

        # Save customer id in session
        request.session["cust_id"] = cust_id

        customer = Customer.objects.get(id=cust_id)

        cart = Cart.objects.filter(user=request.user)

        amount = 0

        for item in cart:
            amount += item.quantity * item.product.discounted_price

        totalamount = amount + 40

        return render(request, "app/payment.html", {
            "customer": customer,
            "cart": cart,
            "totalamount": totalamount,
        })

    return redirect("checkout")
from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderPlaced, Cart

def order_detail(request, pk):
    order = get_object_or_404(
        OrderPlaced,
        id=pk,
        user=request.user
    )

    return render(request, 'app/orderdetail.html', {
        'order': order
    })


def delete_order(request, pk):
    order = get_object_or_404(
        OrderPlaced,
        id=pk,
        user=request.user
    )

    order.delete()

    return redirect('orders')


def buy_again(request, pk):
    order = get_object_or_404(
        OrderPlaced,
        id=pk,
        user=request.user
    )

    product = order.product

    cart = Cart.objects.filter(
        user=request.user,
        product=product
    ).first()

    if cart:
        cart.quantity += 1
        cart.save()
    else:
        Cart.objects.create(
            user=request.user,
            product=product,
            quantity=1
        )

    return redirect('showcart')
def search(request):
    query = request.GET.get('search')

    if query:
        products = Product.objects.filter(title__icontains=query)
    else:
        products = Product.objects.none()

    return render(request, 'app/search.html', {
        'products': products,
        'query': query
    })
def product_detail(request, pk):
    product = Product.objects.get(id=pk)

    return render(request, 'app/productdetail.html', {
        'product': product
    })