from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static  # Importa la función static
from django.urls import path, include
from basededatos.views import login_view, registro_view, inicio
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('items/', include('item.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('inbox/', include('conversation.urls')),
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('login/', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
    path('basededatos/', include('basededatos.urls')),
    path('', inicio, name='inicio'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', include('dashboard.urls', namespace='dashboard')),   
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
