# Generated by Django 3.0.2 on 2020-01-03 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kategorija',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oznaka', models.CharField(max_length=20)),
                ('naziv', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Prodavnica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pib', models.CharField(max_length=20)),
                ('naziv', models.CharField(max_length=50)),
                ('adresa', models.CharField(max_length=40)),
                ('broj_telefona', models.CharField(max_length=30, verbose_name='broj telefona')),
            ],
        ),
        migrations.CreateModel(
            name='Artikal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oznaka', models.CharField(max_length=20)),
                ('naziv', models.CharField(max_length=50)),
                ('opis', models.TextField(max_length=200)),
                ('cena', models.DecimalField(decimal_places=2, max_digits=8)),
                ('na_akciji', models.BooleanField(verbose_name='na akciji')),
                ('kategorije', models.ManyToManyField(to='d3_primeri.Kategorija')),
                ('prodavnica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artikli', to='d3_primeri.Prodavnica')),
            ],
        ),
    ]
