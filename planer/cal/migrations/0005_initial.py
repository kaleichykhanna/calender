# Generated by Django 4.2.6 on 2023-11-01 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cal', '0004_delete_mytable'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=255)),
            ],
        ),
    ]
