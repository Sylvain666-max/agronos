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
    path('blog/', include('blog.urls')),
    path('shop/', include('shop.urls')),
    path('services/', include('services.urls',namespace='services')),
    path("dashboard/", include("dashboard.urls", namespace='dashboard')),
    path('', include('core.urls')),
    path('users',include('users.urls'))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
