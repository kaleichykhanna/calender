# Generated by Django 4.2.6 on 2023-10-31 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cal', '0002_delete_mytable'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monday', models.CharField(max_length=255)),
                ('tuesday', models.CharField(max_length=255)),
                ('wednesday', models.CharField(max_length=255)),
                ('thursday', models.CharField(max_length=255)),
                ('friday', models.CharField(max_length=255)),
                ('saturday', models.CharField(max_length=255)),
                ('sunday', models.CharField(max_length=255)),
            ],
        ),
    ]
