# Generated by Django 4.1.1 on 2023-04-03 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interapp', '0047_remove_resumme_dob'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiztaker',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='quiztaker',
            name='score',
        ),
        migrations.RemoveField(
            model_name='quiztaker',
            name='user',
        ),
        migrations.DeleteModel(
            name='QuizResult',
        ),
        migrations.DeleteModel(
            name='QuizTaker',
        ),
    ]
