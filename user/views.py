from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.models import Profile
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    ProfileSerializer,
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class CreateProfileView(generics.CreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError({"message": "Your image already exists"})


class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
