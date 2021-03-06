# Generated by Django 3.0.3 on 2020-08-30 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0002_auto_20200830_1018'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'verbose_name_plural': 'Stories'},
        ),
        migrations.RenameField(
            model_name='story',
            old_name='supervisor',
            new_name='author',
        ),
        migrations.RemoveField(
            model_name='story',
            name='level',
        ),
        migrations.AddField(
            model_name='story',
            name='topic',
            field=models.CharField(max_length=50, null=True, verbose_name='Topic'),
        ),
    ]
