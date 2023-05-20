from rest_framework import viewsets, mixins

from movies.models import Movie, Actor, Director
from movies.serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    RatingCreateSerializer,
    ActorListSerializer,
    ActorDetailSerializer,
    DirectorListSerializer,
    DirectorDetailSerializer,
)


class MovieViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = MovieListSerializer

    def get_queryset(self):
        queryset = Movie.objects.filter(draft=False)
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MovieDetailSerializer
        return super().get_serializer_class()


class ReviewViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = ReviewCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddStarRatingViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = RatingCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ActorViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ActorDetailSerializer
        return super().get_serializer_class()


class DirectorViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Director.objects.all()
    serializer_class = DirectorListSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DirectorDetailSerializer
        return super().get_serializer_class()
