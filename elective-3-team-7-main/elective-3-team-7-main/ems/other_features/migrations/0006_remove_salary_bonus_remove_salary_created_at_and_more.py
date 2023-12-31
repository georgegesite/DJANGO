# Generated by Django 4.0.6 on 2023-01-11 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('other_features', '0005_alter_salary_bonus_alter_salary_days_logged_in_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salary',
            name='bonus',
        ),
        migrations.RemoveField(
            model_name='salary',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='salary',
            name='days_logged_in',
        ),
        migrations.RemoveField(
            model_name='salary',
            name='salary',
        ),
        migrations.RemoveField(
            model_name='salary',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='salary',
            name='base_salary',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='salary',
            name='withdrawn',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='salary',
            name='working_days',
            field=models.IntegerField(default=0),
        ),
    ]
