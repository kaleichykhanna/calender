# Generated by Django 4.2.6 on 2023-11-02 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0015_plan_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='plan',
            options={'ordering': ['start_time']},
        ),
        migrations.AddField(
            model_name='plan',
            name='end_time',
            field=models.DateTimeField(default='2023-11-02 18:44:51+03:00'),
            preserve_default=False,
        ),
    ]
