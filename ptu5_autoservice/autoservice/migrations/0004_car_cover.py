# Generated by Django 4.1.3 on 2022-11-14 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0003_order_estimate_date_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='covers', verbose_name='cover'),
        ),
    ]