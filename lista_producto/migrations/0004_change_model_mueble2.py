# Generated by Django 4.0.4 on 2022-04-30 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lista_producto', '0003_change_model_mueble'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Mueble',
            new_name='Muebles',
        ),
    ]