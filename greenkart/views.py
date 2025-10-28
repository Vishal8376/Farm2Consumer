from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .models import User, Product, CartItem, Order
from django.contrib import messages

# ---------------------------
# AUTHENTICATION
# ---------------------------
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'greenkart/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            if user.role == 'consumer':
                return redirect('consumer_dashboard')
            elif user.role == 'farmer':
                return redirect('farmer_dashboard')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'greenkart/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

# ---------------------------
# CONSUMER DASHBOARD
# ---------------------------
@login_required
def consumer_dashboard(request):
    products = Product.objects.all()
    return render(request, 'greenkart/consumer_dashboard.html', {'products': products})

# ---------------------------
# CART OPERATIONS
# ---------------------------
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f"{product.name} added to cart!")
    return redirect('consumer_dashboard')


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'greenkart/cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect('view_cart')


# ---------------------------
# PLACE ORDER
# ---------------------------
@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('consumer_dashboard')

    for item in cart_items:
        Order.objects.create(
            buyer=request.user,
            product=item.product,
            quantity=item.quantity,
            total_price=item.product.price * item.quantity,
            status='pending'
        )
    cart_items.delete()
    return render(request, 'greenkart/order_success.html')
# ---------------------------
# FARMER DASHBOARD
# ---------------------------
@login_required
def farmer_dashboard(request):
    if request.user.role != 'farmer':
        return redirect('login')

    products = Product.objects.filter(farmer=request.user)
    return render(request, 'greenkart/farmer_dashboard.html', {'products': products})


@login_required
def add_product(request):
    if request.user.role != 'farmer':
        return redirect('login')

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        location = request.POST.get('location')
        image = request.FILES.get('image')

        Product.objects.create(
            farmer=request.user,
            name=name,
            description=description,
            quantity=quantity,
            price=price,
            location=location,
            image=image
        )
        messages.success(request, "Product added successfully!")
        return redirect('farmer_dashboard')

    return render(request, 'greenkart/add_product.html')


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, farmer=request.user)
    product.delete()
    messages.info(request, "Product deleted successfully.")
    return redirect('farmer_dashboard')
