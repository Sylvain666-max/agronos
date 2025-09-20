from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from agro_site.core.views import home, about, contact_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('a-propos/', about, name='about'),
    path('contact/', contact_view, name='contact'),
    path('blog/', include('agro_site.blog.urls')),
    path('shop/', include('agro_site.shop.urls')),
    path('services/', include('agro_site.services.urls',namespace='services')),
    path("dashboard/", include("agro_site.dashboard.urls", namespace='dashboard')),
    path('', include('agro_site.core.urls')),
    path('users',include('agro_site.users.urls'))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
