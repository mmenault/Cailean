# Generated by Django 4.1.5 on 2023-11-28 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Irori', '0026_remove_personnage_pointsmax'),
    ]

    operations = [
        migrations.AddField(
            model_name='personnage',
            name='Cache',
            field=models.BooleanField(default=False),
        ),
    ]
