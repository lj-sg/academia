from django.urls import path
from .views import items, detail, new, edit, delete, agregar_al_carrito, ver_carrito, quitar_del_carrito, procesar_pago, pago_exitoso
from . import views
app_name = 'item'

urlpatterns = [
    path('', items, name='items'),
    path('<int:pk>/', detail, name='detail'),
    path('new/', new, name='new'),
    path('<int:pk>/edit/', edit, name='edit'),
    path('<int:pk>/delete/', delete, name='delete'),
    path('carrito/', ver_carrito, name='carrito'),
    path('agregar_al_carrito/<int:item_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('quitar_del_carrito/<int:item_id>/', quitar_del_carrito, name='quitar_del_carrito'),
    path('items/', items, name='items'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('pago/', procesar_pago, name='procesar_pago'),
    path('pago_exitoso/', pago_exitoso, name='pago_exitoso'),

]
