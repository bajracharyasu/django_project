# Generated by Django 4.2.1 on 2023-05-16 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MindsetApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('symptoms', models.CharField(max_length=200)),
                ('treatment', models.CharField(max_length=200)),
            ],
        ),
    ]
