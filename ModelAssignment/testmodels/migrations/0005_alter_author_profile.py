# Generated by Django 4.2.9 on 2024-01-31 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testmodels', '0004_collection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='testmodels.profile'),
        ),
    ]