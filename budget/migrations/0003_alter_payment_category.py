# Generated by Django 4.2.5 on 2023-10-01 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_budgetshare_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='category',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]