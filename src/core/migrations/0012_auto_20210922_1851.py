# Generated by Django 2.2.13 on 2021-09-22 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20210922_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='old_works',
            field=models.ManyToManyField(null=True, to='core.Item'),
        ),
    ]