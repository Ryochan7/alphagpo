# Generated by Django 3.2.11 on 2022-01-11 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_category_title_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title_slug',
            field=models.SlugField(editable=False, max_length=1000, unique=True),
        ),
    ]
