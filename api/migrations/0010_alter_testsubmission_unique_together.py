# Generated by Django 5.2.3 on 2025-07-03 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alltesttypes_delete_testtypedb_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='testsubmission',
            unique_together=set(),
        ),
    ]
