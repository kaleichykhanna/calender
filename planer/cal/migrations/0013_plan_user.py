# Generated by Django 4.2.6 on 2023-11-01 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0012_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='plans', to='cal.user'),
            preserve_default=False,
        ),
    ]
