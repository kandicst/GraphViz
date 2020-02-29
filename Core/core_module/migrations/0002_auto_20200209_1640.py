# Generated by Django 3.0.2 on 2020-02-09 15:40

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_module', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='weight',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('30')), django.core.validators.MaxValueValidator(Decimal('70'))]),
        ),
        migrations.AlterField(
            model_name='node',
            name='influence',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('30')), django.core.validators.MaxValueValidator(Decimal('70'))]),
        ),
    ]