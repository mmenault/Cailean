# Generated by Django 4.1.5 on 2023-01-22 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Irori', '0008_typequete_quete'),
    ]

    operations = [
        migrations.AddField(
            model_name='typequete',
            name='Proprietaire',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Irori.personnage'),
        ),
        migrations.AddField(
            model_name='typequete',
            name='Village',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Irori.village'),
        ),
    ]
