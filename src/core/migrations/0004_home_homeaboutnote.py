# Generated by Django 2.2.13 on 2021-09-22 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_banner_selected'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeAboutNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_title', models.CharField(max_length=100)),
                ('small_title', models.CharField(max_length=100)),
                ('about_image', models.ImageField(upload_to='images/')),
                ('banner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Banner')),
                ('notes', models.ManyToManyField(to='core.HomeAboutNote')),
            ],
        ),
    ]
