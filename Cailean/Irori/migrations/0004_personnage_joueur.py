# Generated by Django 4.1.5 on 2023-01-17 21:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Irori', '0003_equipement_quantite_delete_inventaire'),
    ]

    operations = [
        migrations.AddField(
            model_name='personnage',
            name='Joueur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
