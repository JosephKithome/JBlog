# Generated by Django 3.2 on 2021-04-19 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_student'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelTable(
            name='student',
            table='student_info',
        ),
    ]
