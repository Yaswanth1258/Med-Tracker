from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('medicines/', include('medicines.urls')),
    path('', RedirectView.as_view(url='accounts/login/', permanent=False), name='home'),
]
