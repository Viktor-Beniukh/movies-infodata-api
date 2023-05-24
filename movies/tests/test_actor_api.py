from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from movies.models import Actor
from movies.pagination import ApiPagination
from movies.serializers import ActorListSerializer, ActorDetailSerializer


ACTOR_URL = reverse("movies:actor-list")


def sample_actor(**params):
    defaults = {
        "name": "Tom Cruise",
        "age": 60,
        "description": "Test",
    }
    defaults.update(params)

    return Actor.objects.create(**defaults)


def detail_url(actor_id):
    return reverse("movies:actor-detail", args=[actor_id])


class UnauthenticatedActorApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_actors(self):
        sample_actor()
        pagination = ApiPagination

        response = self.client.get(ACTOR_URL)

        actors = Actor.objects.all()
        serializer = ActorListSerializer(pagination, actors, many=True)

        if serializer.is_valid():
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, serializer.data)

    def test_filter_actors_by_name(self):
        sample_actor(name="Tom Cruise")
        sample_actor(name="Arnold Schwarzenegger")
        pagination = ApiPagination

        response = self.client.get(ACTOR_URL, {"name": "Tom Cruise"})

        actors = Actor.objects.filter(name__icontains="tom")
        serializer = ActorListSerializer(pagination, actors, many=True)

        if serializer.is_valid():
            self.assertEqual(response.data, serializer.data)

    def test_retrieve_actor_detail(self):
        actor = sample_actor()

        url = detail_url(actor.id)
        response = self.client.get(url)

        serializer = ActorDetailSerializer(actor)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class AuthenticatedActorApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_create_actor_forbidden(self):
        payload = {
            "name": "Tom Cruise",
            "description": "Description",
            "age": 60,
        }

        response = self.client.post(ACTOR_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminActorApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@test.com",
            "adminpass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_actor(self):

        payload = {
            "name": "Tom Cruise",
            "description": "Description",
            "age": 60,
        }

        response = self.client.post(ACTOR_URL, payload)

        actor = Actor.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(actor, key))
