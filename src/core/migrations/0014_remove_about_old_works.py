# Generated by Django 2.2.13 on 2021-09-22 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_item_sold'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='about',
            name='old_works',
        ),
    ]