# Generated by Django 4.2.1 on 2023-12-20 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboardApp", "0008_alter_todo_options_todo_date_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="todo",
            name="date_created",
            field=models.DateTimeField(blank=True),
        ),
    ]
