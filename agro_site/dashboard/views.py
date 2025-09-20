from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from agro_site.blog.models import Post
from agro_site.shop.models import Product
from agro_site.services.models import Service
from agro_site.dashboard.forms import PostForm, ProductForm, ServiceForm
from django.contrib import messages



def is_dashboard_manager(user):
    return user.is_authenticated and user.groups.filter(name="DashboardManagers").exists()

@login_required
@user_passes_test(is_dashboard_manager)
def dashboard_home(request):
    articles = Post.objects.all()
    products = Product.objects.all()
    services = Service.objects.all()
    context = {
        'articles': articles,
        'products': products,
        'services': services
    }
    return render(request, 'dashboard/base_dashboard.html',context)

# ---------------- Article ----------------
@login_required
@user_passes_test(is_dashboard_manager)
def add_Post(request):
    form =PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('dashboard:dashboard_list_articles')
    return render(request, 'dashboard/add_article.html', {'form': form})

@login_required
@user_passes_test(is_dashboard_manager)
def list_Post(request):
    articles = Post.objects.all()
    return render(request, 'dashboard/list_articles.html', {'articles': articles})

@login_required
@user_passes_test(is_dashboard_manager)
def edit_article(request, pk):
    article = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=article)
    if form.is_valid():
        form.save()
        return redirect('dashboard:dashboard_list_articles')
    return render(request, 'dashboard/add_article.html', {'form': form})

@login_required
@user_passes_test(is_dashboard_manager)
def delete_article(request, pk):
    article = get_object_or_404(Post, pk=pk)
    article.delete()
    return redirect('dashboard:dashboard_list_articles')

# ---------------- Product ----------------
@login_required
@user_passes_test(is_dashboard_manager)
def add_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('dashboard:dashboard_list_products')
    return render(request, 'dashboard/add_product.html', {'form': form})

@login_required
@user_passes_test(is_dashboard_manager)
def list_products(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'dashboard/list_products.html', {'products': products})

@login_required
@user_passes_test(is_dashboard_manager)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('dashboard:dashboard_list_products')
    return render(request, 'dashboard/add_product.html', {'form': form})

@login_required
@user_passes_test(is_dashboard_manager)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_active = False
    product.save()
    messages.success(request, "Produit désactivé avec succès (soft delete).")
    return redirect('dashboard:dashboard_list_products')

# ---------------- Service ----------------
@login_required
@user_passes_test(is_dashboard_manager)
def add_service(request):
    form = ServiceForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('dashboard:dashboard_list_services')
    return render(request, 'dashboard/add_service.html', {'form': form})

@login_required
@user_passes_test(is_dashboard_manager)
def list_services(request):
    services = Service.objects.all()
    return render(request, 'dashboard/list_services.html', {'services': services})

@login_required
@user_passes_test(is_dashboard_manager)
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    form = ServiceForm(request.POST or None, request.FILES or None, instance=service)
    if form.is_valid():
        form.save()
        return redirect('dashboard:dashboard_list_services')
    return render(request, 'dashboard/add_service.html', {'form': form})

@login_required
@user_passes_test(is_dashboard_manager)
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    return redirect('dashboard:dashboard_list_services')

