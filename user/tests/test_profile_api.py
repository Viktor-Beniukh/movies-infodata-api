from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from user.models import Profile


PROFILE_URL = reverse("user:profile-create")


class UnauthenticatedProfileApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(PROFILE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedProfileApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_create_profile(self):
        payload = {
            "user": self.user.email,
        }

        response = self.client.post(PROFILE_URL, payload)

        profile = Profile.objects.get(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(payload["user"], profile.user.email)
