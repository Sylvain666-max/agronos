from pyexpat.errors import messages
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category,VideoPurchase
from .forms import SearchForm
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def post_list(request, category_slug=None):
    posts = Post.objects.filter(published=True)
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)

    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {
        'category': category,
        'page_obj': page_obj
    })



def search(request):
    form = SearchForm(request.GET or None)
    posts = Post.objects.filter(published=True)
    query = ''
    if form.is_valid():
        query = form.cleaned_data.get('q') or ''
        if query:
            posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/search_results.html', {'form': form, 'page_obj': page_obj, 'query': query})




# blog/views.py


stripe.api_key = settings.STRIPE_SECRET_KEY

def post_checkout(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not post.price:
        return redirect(post.get_absolute_url())  # gratuit = pas de paiement

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'xof',  # FCFA
                'product_data': {
                    'name': post.title,
                },
                'unit_amount': int(post.price * 100),  # Stripe attend les centimes
            },
            'quantity': 1,
        }],
        mode='payment',
         success_url=request.build_absolute_uri(reverse('blog:my_courses')) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(
            reverse('blog:cancel')
        ),
        metadata={
            "post_id": str(post.id),   # 🔑 On passe l’ID de la formation achetée
            "user_id": str(request.user.id),
        }
    )
    return redirect(session.url, code=303)


# blog/views.py ou services/views.py selon où tu gères Stripe
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_email = session.get('customer_email')
        post_id = session['metadata']['post_id']  # tu peux passer l’ID de la formation dans metadata
        user = settings.AUTH_USER_MODEL.objects.get(email=user_email)
        post = Post.objects.get(id=post_id)

        VideoPurchase.objects.get_or_create(
            user=user,
            post=post,
            stripe_session_id=session['id'],
            amount=session['amount_total'] / 100
        )
        print("✅ Paiement confirmé pour:", session.get('id'))

    return HttpResponse(status=200)



from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Post, VideoPurchase

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    purchased = False

    #if request.user.is_authenticated:
       # purchased = VideoPurchase.objects.filter(user=request.user, post=post).exists()
    #else:
       # messages.info(request, "Veuillez vous connecter pour accéder à cette formation.")

    context = {
        "post": post,
        "purchased": purchased,
    }

    return render(request, "blog/post_detail.html", context)


@login_required
def my_courses(request):
    purchases = VideoPurchase.objects.filter(user=request.user)
    return render(request, 'blog/my_courses.html', {'purchases': purchases})



def checkout_cancel(request):
    return render(request, 'blog/checkout_cancel.html')
