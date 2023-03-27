# Generated by Django 4.1.1 on 2023-03-27 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interapp', '0031_alter_orderplaced_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='interapp.add_subject'),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='products',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interapp.add_subject'),
        ),
    ]
