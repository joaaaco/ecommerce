# Generated by Django 2.1.2 on 2018-12-05 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20181205_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='administrador',
            field=models.BooleanField(default=False),
        ),
    ]