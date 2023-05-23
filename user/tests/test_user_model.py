from django.contrib.auth import get_user_model
from django.test import TestCase

from user.models import Profile


class ModelsTest(TestCase):

    def test_user_str(self) -> None:
        user = get_user_model().objects.create(
            email="admin@user.com",
            password="admin12345",
            username="Admin"
        )
        self.assertEqual(str(user), user.email)

    def test_profile_str(self) -> None:
        user = get_user_model().objects.create(
            email="admin@user.com",
            password="admin12345",
            username="Admin"
        )
        profile = Profile.objects.create(
            user=user,
            bio="Test profile",
        )
        self.assertEqual(str(profile), str(profile.user))
