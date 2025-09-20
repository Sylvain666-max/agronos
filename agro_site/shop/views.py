from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from agro_site.shop.models import Product, Category, Order, OrderItem
from agro_site.shop.forms import AddToCartForm, CheckoutForm
from agro_site.shop.cart import Cart
from agro_site.shop.models import Order
import stripe
from django.conf import settings







def product_list(request, category_slug=None):
    products = Product.objects.filter(available=True)
    category = None
    query = request.GET.get('q') or ''
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    paginator = Paginator(products.order_by('-created_at'), 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'shop/product_list.html', {'category': category, 'page_obj': page_obj, 'query': query})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    form = AddToCartForm()
    return render(request, 'shop/product_detail.html', {'product': product, 'form': form})

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    cart = Cart(request)
    if request.method == 'POST':
        try:
            qty = int(request.POST.get('quantity', '1'))
        except ValueError:
            qty = 1
        cart.add(product, qty)
    return redirect('shop:cart_detail')

def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('shop:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart.html', {'cart': cart})

def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('shop:product_list')
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return redirect('shop:checkout_order', order_id=order.id)
    else:
        form = CheckoutForm()
    return render(request, 'shop/checkout.html', {'cart': cart, 'form': form})


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.paid = True
    order.save()
    return render(request, 'shop/order_success.html', {'order': order})


# shop/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
import stripe
from agro_site.shop.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Création session Stripe Checkout
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                "price_data": {
                    "currency": "xof",  # adapte si besoin
                    "product_data": {
                        "name": f"Commande n°{order.id}",
                    },
                    "unit_amount": int(order.get_total_cost() * 100),  # montant total en centimes
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri(
            f'/shop/order-success/{order.id}/'
        ),
        cancel_url=request.build_absolute_uri(
            f'/shop/order/cancel/{order.id}/'
        ),
    )

    # Redirection Stripe
    return redirect(session.url, code=303)


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = "paid"   # ⚡ Mets à jour le statut
    order.save()
    return render(request, "shop/order_success.html", {"order": order})


def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "shop/order_cancel.html", {"order": order})
