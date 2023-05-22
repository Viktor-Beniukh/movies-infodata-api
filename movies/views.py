from django.db.models import Avg
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from movies.models import Movie, Actor, Director, Category, Genre, MovieFrames
from movies.pagination import ApiPagination
from movies.permissions import IsAdminOrReadOnly

from movies.serializers import (
    MovieSerializer,
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    RatingCreateSerializer,
    ActorSerializer,
    ActorListSerializer,
    ActorDetailSerializer,
    DirectorSerializer,
    DirectorListSerializer,
    DirectorDetailSerializer,
    CategoryCreateSerializer,
    GenreCreateSerializer,
    MovieFramesSerializer,
)
from movies.service import MovieFilter


class MovieViewSet(viewsets.ModelViewSet):
    queryset = (
        Movie.objects.filter(draft=False)
        .annotate(average_rating=Avg("film_rating__star__value"))
    )
    serializer_class = MovieSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    pagination_class = ApiPagination

    def get_queryset(self):
        title = self.request.query_params.get("title")
        category = self.request.query_params.get("category")
        queryset = super().get_queryset()

        if title:
            queryset = queryset.filter(title__icontains=title)

        if category:
            queryset = queryset.filter(category__name__icontains=category)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer
        if self.action == "retrieve":
            return MovieDetailSerializer
        return super().get_serializer_class()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="title",
                type=str,
                description=(
                    "Filter by title (ex. ?title=Terminator)"
                )
            ),
            OpenApiParameter(
                name="category",
                type=str,
                description=(
                    "Filter by category name (ex. ?category=Films)"
                )
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ReviewViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = ReviewCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddStarRatingViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = RatingCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = ApiPagination

    def get_queryset(self):
        name = self.request.query_params.get("name")
        queryset = super().get_queryset()

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ActorListSerializer
        if self.action == "retrieve":
            return ActorDetailSerializer
        return super().get_serializer_class()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                type=str,
                description=(
                    "Filter by name (ex. ?name=Tom Cruise)"
                )
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = ApiPagination

    def get_queryset(self):
        name = self.request.query_params.get("name")
        queryset = super().get_queryset()

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return DirectorListSerializer
        if self.action == "retrieve":
            return DirectorDetailSerializer
        return super().get_serializer_class()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                type=str,
                description=(
                    "Filter by name (ex. ?name=James Cameron)"
                )
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CategoryViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    permission_classes = (IsAdminUser,)


class GenreViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreCreateSerializer
    permission_classes = (IsAdminUser,)


class MovieFramesViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = MovieFrames.objects.select_related("movies")
    serializer_class = MovieFramesSerializer
    permission_classes = (IsAdminUser,)
