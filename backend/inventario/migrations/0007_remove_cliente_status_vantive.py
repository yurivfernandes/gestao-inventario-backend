# Generated by Django 4.2.10 on 2025-01-24 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0006_remove_site_tipo_negocio_site_cnpj_site_razao_social'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='status_vantive',
        ),
    ]
