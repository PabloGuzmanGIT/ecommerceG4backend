# Generated by Django 4.0.4 on 2022-05-16 23:14

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lista_producto', '0004_change_model_mueble2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ruta', cloudinary.models.CloudinaryField(max_length=255)),
                ('muebleId', models.ForeignKey(db_column='mueble_id', on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='lista_producto.muebles')),
            ],
            options={
                'db_table': 'pictures',
            },
        ),
    ]
