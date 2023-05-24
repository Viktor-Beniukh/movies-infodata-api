from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient


from movies.models import Movie, RatingStar, Rating


RATING_URL = reverse("movies:ratings-list")


def sample_movie(**params):
    defaults = {
        "title": "Sample movie",
        "description": "Sample description",
        "year_of_release": 1990,
    }
    defaults.update(params)

    return Movie.objects.create(**defaults)


def sample_star(**params):
    defaults = {
        "value": 3,
    }
    defaults.update(params)

    return RatingStar.objects.create(**defaults)


class UnauthenticatedRatingsApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(RATING_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRatingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_create_rating(self):
        movie = sample_movie()
        star = sample_star()

        payload = {
            "star": star.value,
            "movie": movie.id,
        }

        response = self.client.post(RATING_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        rating = Rating.objects.get(user=self.user, movie=movie)

        for key in payload:
            self.assertEqual(payload[key], getattr(rating, key).id)
