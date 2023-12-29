from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

@receiver(post_save, sender=User)
def asignar_grupo_usuarios_normales(sender, instance, created, **kwargs):
    if created:
        grupo_usuarios_normales = Group.objects.get(name='UsuariosNormales')
        instance.groups.add(grupo_usuarios_normales)