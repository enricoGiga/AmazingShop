from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from products_store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('supplier/', views.supplier_dashboard, name='supplier_dashboard'),
    path('buyer/', views.buyer_dashboard, name='buyer_dashboard'),
    path('login/', views.CustomLoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),
         name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
