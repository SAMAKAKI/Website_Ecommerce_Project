# Generated by Django 4.1.7 on 2023-03-11 17:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('locality', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=50)),
                ('mobile', models.IntegerField(default=0)),
                ('zipcode', models.IntegerField()),
                ('state', models.CharField(choices=[('Dolnośląskie', 'Dolnośląskie'), ('Kujawsko-pomorskie', 'Kujawsko-pomorskie'), ('Lubelskie', 'Lubelskie'), ('Lubuskie', 'Lubuskie'), ('Łódzkie', 'Łódzkie'), ('Małopolskie', 'Małopolskie'), ('Mazowieckie', 'Mazowieckie'), ('Opolskie', 'Opolskie'), ('Podkarpackie', 'Podkarpackie'), ('Podlaskie', 'Podlaskie'), ('Pomorskie', 'Pomorskie'), ('Śląskie', 'Śląskie'), ('Świętokrzyskie', 'Świętokrzyskie'), ('Warmińsko-mazurskie', 'Warmińsko-mazurskie'), ('Wielkopolskie', 'Wielkopolskie'), ('Zachodniopomorskie', 'Zachodniopomorskie')], max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]