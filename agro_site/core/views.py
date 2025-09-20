from django.shortcuts import render, redirect
from agro_site.blog.models import Post
from agro_site.shop.models import Product
from agro_site.services.models import Service
from agro_site.core.forms import ContactForm
from django.contrib import messages

def home(request):
    # Contenu normal de la page
    posts = Post.objects.filter(published=True).order_by('-created_at')[:6]
    products = Product.objects.filter(available=True).order_by('-created_at')[:8]
    services = Service.objects.all()[:6]

    # Vérifie si l'utilisateur est un dashboard manager
    is_dashboard_manager = False
    if request.user.is_authenticated:
        is_dashboard_manager = request.user.groups.filter(name="DashboardManagers").exists()

    context = {
        'posts': posts,
        'products': products,
        'services': services,
        'is_dashboard_manager': is_dashboard_manager,
    }

    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Merci ! Votre message a bien été envoyé.")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})


from django.shortcuts import render

def mentions_legales(request):
    return render(request, 'core/mentions_legales.html')
