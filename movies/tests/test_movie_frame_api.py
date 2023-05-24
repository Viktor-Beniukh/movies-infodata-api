from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from movies.models import Movie, MovieFrames


MOVIE_FRAME_URL = reverse("movies:movie-frames-list")


def sample_movie_frame(**params):
    movie = sample_movie()

    defaults = {
        "title": "Sample movie frame",
        "movies": movie
    }
    defaults.update(params)

    return MovieFrames.objects.create(**defaults)


def sample_movie(**params):
    defaults = {
        "title": "Sample movie",
        "description": "Sample description",
        "year_of_release": 1990,
    }
    defaults.update(params)

    return Movie.objects.create(**defaults)


class UnauthenticatedMovieFrameApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(MOVIE_FRAME_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedMovieFrameApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_create_movie_frame_forbidden(self):
        payload = {
            "title": "Movie Frame",
            "description": "Description",
        }

        response = self.client.post(MOVIE_FRAME_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminMovieFrameApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@test.com",
            "adminpass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_movie_frame(self):
        movie_frame = sample_movie_frame()
        movie = sample_movie()

        payload = {
            "title": movie_frame.title,
            "movies": movie.id,
        }

        response = self.client.post(MOVIE_FRAME_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        frame = MovieFrames.objects.get(
            title=response.data["title"], movies=movie.id
        )

        for key in payload:
            if key == "movies":
                self.assertEqual(int(payload[key]), getattr(frame, key).id)
            else:
                self.assertEqual(payload[key], str(getattr(frame, key)))
