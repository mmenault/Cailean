# Generated by Django 4.1.5 on 2023-01-17 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Caracteristique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=64)),
                ('Points', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Personnage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Prenom', models.CharField(max_length=64)),
                ('Nom', models.CharField(max_length=64)),
                ('Age', models.IntegerField()),
                ('Sexe', models.CharField(max_length=64)),
                ('Nationalite', models.CharField(max_length=64)),
                ('Personnalite', models.CharField(max_length=64)),
                ('Profession', models.CharField(max_length=64)),
                ('Specialite', models.CharField(max_length=64)),
                ('Aime', models.CharField(max_length=64)),
                ('Deteste', models.CharField(max_length=64)),
                ('PvMax', models.IntegerField()),
                ('Pv', models.IntegerField()),
                ('PpMax', models.IntegerField()),
                ('Pp', models.IntegerField()),
                ('MoralMax', models.IntegerField()),
                ('Moral', models.IntegerField()),
                ('PointsRestant', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Qualite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Pouvoir',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=64)),
                ('Description', models.CharField(max_length=64)),
                ('Niveau', models.IntegerField()),
                ('Cout', models.IntegerField()),
                ('Proprietaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Irori.personnage')),
            ],
        ),
        migrations.CreateModel(
            name='Inventaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=64)),
                ('Proprietaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Irori.personnage')),
                ('Qualite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Irori.qualite')),
            ],
        ),
        migrations.CreateModel(
            name='Equipement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=64)),
                ('Description', models.CharField(max_length=64)),
                ('Statistique', models.CharField(max_length=64)),
                ('Proprietaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Irori.personnage')),
                ('Qualite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Irori.qualite')),
            ],
        ),
        migrations.CreateModel(
            name='Competence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=64)),
                ('Bonus', models.IntegerField()),
                ('Categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Irori.caracteristique')),
            ],
        ),
        migrations.AddField(
            model_name='caracteristique',
            name='Proprietaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Irori.personnage'),
        ),
    ]