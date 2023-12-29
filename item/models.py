from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # Nuevos campos para el carrito
    quantity_available = models.PositiveIntegerField(default=1)  # Cantidad disponible en inventario

    def vender(self, cantidad):
        if self.quantity_available >= cantidad:
            self.quantity_available -= cantidad
            self.save()
            return True
        else:
            return False

    def __str__(self):
        return self.name

class CarritoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def subtotal(self):
        return self.quantity * self.product.price
    
class TransaccionPago(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_cliente = models.CharField(max_length=100)
    nit_cliente = models.CharField(max_length=15)
    direccion_cliente = models.CharField(max_length=255)
    # Agrega otros campos según sea necesario

    def __str__(self):
        return f'Transacción de Pago de {self.nombre_cliente} ({self.nit_cliente}) por {self.usuario.username}'
    

class ItemComprado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ['usuario', 'item']
        
    def __str__(self):
        return f'{self.cantidad} x {self.item.name}'