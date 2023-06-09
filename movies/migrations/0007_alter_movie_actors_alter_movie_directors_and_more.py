# Generated by Django 4.2.1 on 2023-05-22 17:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0006_alter_movie_actors_alter_movie_directors_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="actors",
            field=models.ManyToManyField(
                blank=True, related_name="film_actor", to="movies.actor"
            ),
        ),
        migrations.AlterField(
            model_name="movie",
            name="directors",
            field=models.ManyToManyField(
                blank=True, related_name="film_director", to="movies.director"
            ),
        ),
        migrations.AlterField(
            model_name="movie",
            name="genres",
            field=models.ManyToManyField(
                blank=True, related_name="film_genre", to="movies.genre"
            ),
        ),
    ]
