# Generated by Django 3.2.5 on 2021-07-14 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes_app', '0002_rename_description_note_content'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ['-last_save_time']},
        ),
    ]
