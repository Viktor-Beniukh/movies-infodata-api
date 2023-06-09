# Generated by Django 4.2.1 on 2023-05-23 09:35

from django.db import migrations, models
import movies.models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0007_alter_movie_actors_alter_movie_directors_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="actor",
            name="image",
            field=models.ImageField(
                null=True, upload_to=movies.models.actor_image_file_path
            ),
        ),
        migrations.AlterField(
            model_name="director",
            name="image",
            field=models.ImageField(
                null=True, upload_to=movies.models.director_image_file_path
            ),
        ),
        migrations.AlterField(
            model_name="movie",
            name="poster",
            field=models.ImageField(
                null=True, upload_to=movies.models.movie_image_file_path
            ),
        ),
        migrations.AlterField(
            model_name="movieframes",
            name="image",
            field=models.ImageField(
                null=True, upload_to=movies.models.movie_frames_image_file_path
            ),
        ),
    ]
