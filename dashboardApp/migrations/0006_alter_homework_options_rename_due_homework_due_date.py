# Generated by Django 4.2.1 on 2023-12-19 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "dashboardApp",
            "0005_alter_homework_options_remove_homework_updated_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="homework",
            options={"ordering": ("-due_date", "-created")},
        ),
        migrations.RenameField(
            model_name="homework",
            old_name="due",
            new_name="due_date",
        ),
    ]
