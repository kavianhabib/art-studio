# Generated by Django 2.2.13 on 2021-09-22 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_home_homeaboutnote'),
    ]

    operations = [
        migrations.AddField(
            model_name='home',
            name='purchase_now_description',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='home',
            name='purchase_now_title',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
