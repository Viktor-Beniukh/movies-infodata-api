from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from movies.models import Director
from movies.pagination import ApiPagination
from movies.serializers import DirectorListSerializer, DirectorDetailSerializer


DIRECTOR_URL = reverse("movies:director-list")


def sample_director(**params):
    defaults = {
        "name": "Steven Spielberg",
        "age": 70,
        "description": "Test",
    }
    defaults.update(params)

    return Director.objects.create(**defaults)


def detail_url(director_id):
    return reverse("movies:director-detail", args=[director_id])


class UnauthenticatedDirectorApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_directors(self):
        sample_director()
        pagination = ApiPagination

        response = self.client.get(DIRECTOR_URL)

        directors = Director.objects.all()
        serializer = DirectorListSerializer(pagination, directors, many=True)

        if serializer.is_valid():
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, serializer.data)

    def test_filter_directors_by_name(self):
        sample_director(name="Steven Spielberg")
        sample_director(name="James Cameron")
        pagination = ApiPagination

        response = self.client.get(DIRECTOR_URL, {"name": "James Cameron"})

        directors = Director.objects.filter(name__icontains="jam")
        serializer = DirectorListSerializer(pagination, directors, many=True)

        if serializer.is_valid():
            self.assertEqual(response.data, serializer.data)

    def test_retrieve_director_detail(self):
        director = sample_director()

        url = detail_url(director.id)
        response = self.client.get(url)

        serializer = DirectorDetailSerializer(director)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class AuthenticatedDirectorApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_create_director_forbidden(self):
        payload = {
            "name": "Steven Spielberg",
            "description": "Description",
            "age": 70,
        }

        response = self.client.post(DIRECTOR_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminDirectorApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@test.com",
            "adminpass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_director(self):

        payload = {
            "name": "Steven Spielberg",
            "description": "Description",
            "age": 70,
        }

        response = self.client.post(DIRECTOR_URL, payload)

        director = Director.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(director, key))
