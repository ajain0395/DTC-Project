# Generated by Django 2.2.1 on 2019-07-27 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stops',
            options={'ordering': ('stop_id', 'stop_code', 'stop_name', 'geometr'), 'verbose_name_plural': 'stops'},
        ),
        migrations.RenameField(
            model_name='stops',
            old_name='geometry',
            new_name='geometr',
        ),
    ]
