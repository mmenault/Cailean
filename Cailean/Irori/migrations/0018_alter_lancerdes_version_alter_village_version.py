# Generated by Django 4.1.5 on 2023-11-04 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Irori', '0017_lancerdes_version_village_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lancerdes',
            name='Version',
            field=models.IntegerField(default=4),
        ),
        migrations.AlterField(
            model_name='village',
            name='Version',
            field=models.IntegerField(default=4),
        ),
    ]
