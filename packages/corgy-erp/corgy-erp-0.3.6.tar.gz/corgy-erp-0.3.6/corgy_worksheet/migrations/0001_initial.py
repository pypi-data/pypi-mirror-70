# Generated by Django 3.0.6 on 2020-06-01 01:31

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('corgy_mdm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='work', max_length=100)),
            ],
            options={
                'verbose_name': 'activity',
            },
        ),
        migrations.CreateModel(
            name='WorksheetModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corgy_mdm.PersonModel')),
            ],
            options={
                'verbose_name': 'worksheet',
            },
        ),
        migrations.CreateModel(
            name='WorksheetEntryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('duration', models.DurationField(default=datetime.timedelta(0))),
                ('note', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('activity', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logged_entries', to='corgy_worksheet.ActivityModel')),
                ('worksheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='corgy_worksheet.WorksheetModel')),
            ],
        ),
    ]
