from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from movies.models import Movie, Actor, Director, Category, Genre, MovieFrames

from movies.serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    RatingCreateSerializer,
    ActorListSerializer,
    ActorDetailSerializer,
    DirectorListSerializer,
    DirectorDetailSerializer,
    CategoryCreateSerializer,
    GenreCreateSerializer,
    MovieFramesSerializer,
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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddStarRatingViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = RatingCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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


class CategoryViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)


class GenreViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)


class MovieFramesViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = MovieFrames.objects.all()
    serializer_class = MovieFramesSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
