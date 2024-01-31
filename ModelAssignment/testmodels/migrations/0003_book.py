# Generated by Django 4.2.9 on 2024-01-31 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testmodels', '0002_publisher'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('title', models.CharField(max_length=255)),
                ('date_of_pub', models.DateTimeField(verbose_name='Published Date')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testmodels.author')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testmodels.publisher')),
            ],
        ),
    ]
