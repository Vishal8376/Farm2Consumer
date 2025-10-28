from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .models import User, Product, CartItem, Order


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
                return redirect('login')
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
    cart_count = CartItem.objects.filter(user=request.user).count()
    return render(request, 'greenkart/consumer_dashboard.html', {
        'products': products,
        'cart_count': cart_count
    })


# ---------------------------
# CART OPERATIONS
# ---------------------------
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity = min(cart_item.quantity + 1, product.quantity)
    cart_item.save()

    return redirect(request.META.get('HTTP_REFERER', 'consumer_dashboard'))


def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = 0
    for item in cart_items:
        item.line_total = item.product.price * item.quantity  # add field for template
        total += item.line_total

    return render(request, 'greenkart/cart.html', {
        'cart_items': cart_items,
        'total': total
    })




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
        return redirect('farmer_dashboard')

    return render(request, 'greenkart/add_product.html')


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, farmer=request.user)
    product.delete()
    return redirect('farmer_dashboard')

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.image = request.FILES.get('image') or product.image
        product.save()
        return redirect('farmer_dashboard')

    return render(request, 'greenkart/edit_product.html', {'product': product})
from decimal import Decimal
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import CartItem, Order, Product, Payment
import uuid

# Show checkout page (cart review + dummy payment form)
@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('consumer_dashboard')

    # compute per-line and total
    total = Decimal('0.00')
    for item in cart_items:
        item.line_total = (item.product.price * item.quantity).quantize(Decimal('0.01'))
        total += item.line_total

    total = total.quantize(Decimal('0.01'))

    return render(request, 'greenkart/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })

# Process (simulate) payment — POST request
@login_required
def process_payment(request):
    if request.method != 'POST':
        return redirect('checkout')

    # Very basic validation of "card" fields (dummy)
    card_name = request.POST.get('card_name', '').strip()
    card_number = request.POST.get('card_number', '').strip()
    expiry = request.POST.get('expiry', '').strip()
    cvv = request.POST.get('cvv', '').strip()

    if not (card_name and card_number and expiry and cvv):
        # invalid — you can use messages framework or redirect with error
        return redirect('checkout')

    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('consumer_dashboard')

    # compute total
    total = Decimal('0.00')
    for item in cart_items:
        item.line_total = (item.product.price * item.quantity).quantize(Decimal('0.01'))
        total += item.line_total
    total = total.quantize(Decimal('0.01'))

    # create payment record (pending -> then paid)
    txid = uuid.uuid4().hex
    payment = Payment.objects.create(
        transaction_id=txid,
        buyer=request.user,
        amount=total,
        status='pending',
        method='dummy-card',
        notes=f'Card ending {card_number[-4:]}'
    )

    # simulate processing — always success in dummy gateway
    # wrap order creation + payment update in atomic transaction
    try:
        with transaction.atomic():
            payment.status = 'paid'
            payment.save()

            # create orders, one per cart item
            for item in cart_items:
                Order.objects.create(
                    buyer=request.user,
                    product=item.product,
                    quantity=item.quantity,
                    total_price=item.product.price * item.quantity,
                    status='pending'
                )
            # clear cart
            cart_items.delete()
    except Exception as e:
        payment.status = 'failed'
        payment.save()
        # optionally log e
        return redirect('checkout')

    # success
    return redirect(reverse('payment_success', args=[payment.transaction_id]))


# Payment success view
@login_required
def payment_success(request, txid):
    payment = get_object_or_404(Payment, transaction_id=txid, buyer=request.user)
    return render(request, 'greenkart/payment_success.html', {
        'payment': payment
    })
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order

@login_required
def consumer_orders(request):
    orders = Order.objects.filter(consumer=request.user).order_by('-created_at')
    return render(request, 'greenkart/orders.html', {'orders': orders})
