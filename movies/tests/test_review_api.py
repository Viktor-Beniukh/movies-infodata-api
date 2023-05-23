from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from movies.models import Review, Movie


REVIEW_URL = reverse("movies:reviews-list")


def sample_movie(**params):
    defaults = {
        "title": "Sample movie",
        "description": "Sample description",
        "year_of_release": 1990,
    }
    defaults.update(params)

    return Movie.objects.create(**defaults)


class AuthenticatedReviewApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_create_review(self):
        movie = sample_movie()

        payload = {
            "text": "Great",
            "movie": movie.id,
            "parent": ""

        }

        response = self.client.post(REVIEW_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)

        review_exists = Review.objects.filter(user=self.user).exists()
        self.assertTrue(review_exists)
