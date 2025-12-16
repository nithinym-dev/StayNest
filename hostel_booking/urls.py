from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def serviceworker(request):
    return HttpResponse("// Empty service worker", content_type="application/javascript")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('serviceworker.js', serviceworker, name='serviceworker'),  # Add this line
    path('', include('accounts.urls')),
    path('properties/', include('properties.urls')),
    path('bookings/', include('bookings.urls')),
    path('payments/', include('payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
