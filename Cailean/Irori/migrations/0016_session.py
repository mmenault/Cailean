# Generated by Django 4.1.5 on 2023-03-23 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Irori', '0015_lancerdes_session'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Numero', models.IntegerField(default=1)),
            ],
        ),
    ]
