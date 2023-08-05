# Generated by Django 2.2.3 on 2019-11-28 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("response", "0014_event")]

    operations = [
        migrations.AddField(
            model_name="action",
            name="created_date",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="action", name="done_date", field=models.DateTimeField(null=True)
        ),
        migrations.AddField(
            model_name="action", name="due_date", field=models.DateTimeField(null=True)
        ),
        migrations.AddField(
            model_name="action",
            name="priority",
            field=models.CharField(
                blank=True,
                choices=[("1", "high"), ("2", "medium"), ("3", "low")],
                max_length=10,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="action",
            name="type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("1", "detective"),
                    ("2", "preventative"),
                    ("3", "corrective"),
                ],
                max_length=10,
                null=True,
            ),
        ),
    ]
