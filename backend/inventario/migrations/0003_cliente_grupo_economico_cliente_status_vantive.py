# Generated by Django 4.2.10 on 2025-01-20 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_grupoeconomico_alter_cliente_cnpj_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='grupo_economico',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='inventario.grupoeconomico'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cliente',
            name='status_vantive',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
