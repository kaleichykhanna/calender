# Generated by Django 4.2.6 on 2023-11-25 14:00

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cal', '0019_event_habit_delete_plan_event_name_event_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('start_time_monday', models.TimeField(blank=True, null=True)),
                ('end_time_monday', models.TimeField(blank=True, null=True)),
                ('start_time_tuesday', models.TimeField(blank=True, null=True)),
                ('end_time_tuesday', models.TimeField(blank=True, null=True)),
                ('start_time_wednesday', models.TimeField(blank=True, null=True)),
                ('end_time_wednesday', models.TimeField(blank=True, null=True)),
                ('start_time_thursday', models.TimeField(blank=True, null=True)),
                ('end_time_thursday', models.TimeField(blank=True, null=True)),
                ('start_time_friday', models.TimeField(blank=True, null=True)),
                ('end_time_friday', models.TimeField(blank=True, null=True)),
                ('start_time_saturday', models.TimeField(blank=True, null=True)),
                ('end_time_saturday', models.TimeField(blank=True, null=True)),
                ('start_time_sunday', models.TimeField(blank=True, null=True)),
                ('end_time_sunday', models.TimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hours', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('hour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hours', to='cal.hour')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plans', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='habit',
            name='id',
        ),
        migrations.RemoveField(
            model_name='habit',
            name='name',
        ),
        migrations.AddField(
            model_name='habit',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2024, 1, 24, 14, 0, 11, 651616, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('plan_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cal.plan')),
                ('due_date', models.DateField()),
            ],
            bases=('cal.plan',),
        ),
        migrations.AddField(
            model_name='habit',
            name='plan_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cal.plan'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='names', to='cal.plan'),
        ),
    ]