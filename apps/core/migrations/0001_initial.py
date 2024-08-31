# Generated by Django 5.1 on 2024-08-31 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('dob', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[
                 ('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=10)),
                ('role', models.CharField(choices=[('super_admin', 'Super Admin'), (
                    'artist_manager', 'Artist Manager'), ('artist', 'Artist')], default='super_admin', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
