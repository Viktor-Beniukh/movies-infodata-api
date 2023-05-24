from django.contrib.auth import get_user_model
from django.test import TestCase

from movies.models import (
    Movie,
    Category,
    Actor,
    Director,
    Genre,
    MovieFrames,
    RatingStar,
    Rating,
    Review
)


class ModelsTest(TestCase):

    def test_movie_str(self) -> None:
        movie = Movie.objects.create(
            title="Terminator",
        )
        self.assertEqual(str(movie), movie.title)

    def test_movie_frame_str(self) -> None:
        movie = Movie.objects.create(
            title="Terminator",
        )
        movie_frame = MovieFrames.objects.create(
            title="Test frame",
            movies=movie
        )
        self.assertEqual(str(movie_frame), movie_frame.title)

    def test_category_str(self) -> None:
        category = Category.objects.create(
            name="Cartoon"
        )
        self.assertEqual(str(category), category.name)

    def test_genre_str(self) -> None:
        genre = Genre.objects.create(
            name="Action"
        )
        self.assertEqual(str(genre), genre.name)

    def test_actor_str(self) -> None:
        actor = Actor.objects.create(
            name="Tom Cruise"
        )
        self.assertEqual(str(actor), actor.name)

    def test_director_str(self) -> None:
        director = Director.objects.create(
            name="Steven Spielberg"
        )
        self.assertEqual(str(director), director.name)

    def test_rating_star_str(self) -> None:
        star = RatingStar.objects.create(
            value=4
        )
        self.assertEqual(str(star), str(star.value))

    def test_rating_str(self) -> None:
        user = get_user_model().objects.create_user(
            email="admin@user.com",
            password="admin12345",
        )
        star = RatingStar.objects.create(
            value=4
        )
        movie = Movie.objects.create(
            title="Terminator",
        )
        rating = Rating.objects.create(
            user=user,
            movie=movie,
            star=star
        )
        self.assertEqual(f"{star} - {movie}", f"{rating.star} - {rating.movie}")

    def test_review_str(self) -> None:
        user = get_user_model().objects.create_user(
            email="admin@user.com",
            password="admin12345",
        )
        movie = Movie.objects.create(
            title="Terminator",
        )
        review = Review.objects.create(
            user=user,
            movie=movie,
            text="This is a good film"
        )
        self.assertEqual(f"{user} - {movie}", f"{review.user} - {review.movie}")
