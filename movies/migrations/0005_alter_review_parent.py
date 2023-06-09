# Generated by Django 4.2.1 on 2023-05-21 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0004_alter_ratingstar_value"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="children",
                to="movies.review",
                verbose_name="Parent",
            ),
        ),
    ]
