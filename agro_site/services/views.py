from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Service, Purchase
from .forms import QuoteForm
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import logging

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Logger pour debug
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Liste des services
def service_list(request):
    services = Service.objects.all()
    return render(request, 'services/service_list.html', {'services': services})

# Détail d'un service + formulaire de devis
def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.service = service
            quote.save()
            messages.success(request, "Votre demande de devis a été envoyée.")
            return redirect(service.get_absolute_url())
    else:
        form = QuoteForm()
    
    return render(request, 'services/service_detail.html', {'service': service, 'form': form})

# Création d'une session Stripe Checkout
def create_checkout_session(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if not service.price_from:
        messages.error(request, "Ce service n'a pas de prix défini.")
        return redirect(service.get_absolute_url())
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'xof',  
                'product_data': {'name': service.name},
                'unit_amount': int(service.price_from * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/services/success/'),
        cancel_url=request.build_absolute_uri(service.get_absolute_url()),
        metadata={'service_id': service.id},  # pour identifier le service dans le webhook
    )
    
    return redirect(session.url)

# Webhook Stripe
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        logger.error(f"⚠️ Payload invalide: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"⚠️ Signature invalide: {e}")
        return HttpResponse(status=400)

    logger.info(f"✅ Webhook reçu : {event['type']}")
    
    # Paiement réussi
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        try:
            service_id = session['metadata']['service_id']
            service = Service.objects.get(id=service_id)
            Purchase.objects.create(
                service=service,
                stripe_session_id=session['id'],
                amount=session['amount_total'] / 100,
                customer_email=session.get('customer_email', 'inconnu@example.com'),
            )
            logger.info(f"💰 Achat enregistré pour {service.name}")
        except Service.DoesNotExist:
            logger.warning(f"⚠️ Service non trouvé pour l'ID {service_id}")

    return HttpResponse(status=200)

# Page de succès après paiement
def success_payment(request):
    return render(request, 'services/services_success.html')
