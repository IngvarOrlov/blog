# Generated by Django 5.0.4 on 2024-05-09 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0002_profile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Профиль пользователя'},
        ),
    ]
