# Generated by Django 4.1.2 on 2023-01-29 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("goals", "0004_alter_goalcategory_board"),
    ]

    operations = [
        migrations.AlterField(
            model_name="goal",
            name="description",
            field=models.TextField(blank=True, null=True, verbose_name="Описание"),
        ),
    ]
