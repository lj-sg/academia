# Generated by Django 4.2.5 on 2023-12-29 08:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('item', '0006_itemcomprado'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='itemcomprado',
            unique_together={('usuario', 'item')},
        ),
    ]
