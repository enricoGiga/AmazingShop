# Generated by Django 5.1.1 on 2024-09-26 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='main_image',
            field=models.ImageField(blank=True, null=True, upload_to='products/images/'),
        ),
    ]
