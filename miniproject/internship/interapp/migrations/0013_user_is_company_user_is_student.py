# Generated by Django 4.1.1 on 2023-02-23 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interapp', '0012_remove_user_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_company',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_student',
            field=models.BooleanField(default=False),
        ),
    ]
