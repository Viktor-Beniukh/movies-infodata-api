import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


def actor_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/actors/", filename)


class Actor(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=actor_image_file_path, null=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


def director_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/directors/", filename)


class Director(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=director_image_file_path, null=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


def movie_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/movies/", filename)


class Movie(models.Model):
    title = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    poster = models.ImageField(upload_to=movie_image_file_path, null=True)
    year_of_release = models.PositiveSmallIntegerField(default=2019)
    country = models.CharField(max_length=255, blank=True)
    directors = models.ManyToManyField(Director, related_name="film_director", blank=True)
    actors = models.ManyToManyField(Actor, related_name="film_actor", blank=True)
    genres = models.ManyToManyField(Genre, related_name="film_genre", blank=True)
    world_premiere = models.DateField(null=True, blank=True)
    budget = models.PositiveIntegerField(
        default=0, help_text="Enter amount in dollars"
    )
    fees_in_the_usa = models.PositiveIntegerField(
        default=0, help_text="Enter amount in dollars"
    )
    fees_in_the_world = models.PositiveIntegerField(
        default=0, help_text="Enter amount in dollars"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="film_category"
    )
    draft = models.BooleanField(default=False)

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return self.title

    def get_review(self):
        return self.reviews.filter(parent__isnull=True)


def movie_frames_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/movie-frames/", filename)


class MovieFrames(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=movie_frames_image_file_path, null=True)
    movies = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="film_shots"
    )

    class Meta:
        ordering = ("title",)
        verbose_name = "Movie frame"
        verbose_name_plural = "Movie frames"

    def __str__(self):
        return self.title


class RatingStar(models.Model):
    value = models.IntegerField()

    class Meta:
        ordering = ("-value",)

    def __str__(self):
        return str(self.value)


class Rating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_rating"
    )
    star = models.ForeignKey(
        RatingStar, on_delete=models.CASCADE, related_name="star_rating"
    )
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="film_rating"
    )

    def __str__(self):
        return f"{self.star} - {self.movie}"


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_review"
    )
    text = models.TextField(blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Parent",
        related_name="children"
    )
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="reviews"
    )

    def __str__(self):
        return f"{self.user} - {self.movie}"
