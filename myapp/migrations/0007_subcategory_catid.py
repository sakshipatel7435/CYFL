# Generated by Django 5.1.4 on 2025-03-27 13:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_remove_category_subcatid'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='catid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.category'),
        ),
    ]
