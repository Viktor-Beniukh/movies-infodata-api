from django.db.models import Avg
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from movies.models import Movie, Actor, Director, Category, Genre, MovieFrames
from movies.pagination import ApiPagination
from movies.permissions import IsAdminOrReadOnly

from movies.serializers import (
    MovieSerializer,
    MovieListSerializer,
    MovieDetailSerializer,
    MoviePosterSerializer,
    ReviewCreateSerializer,
    RatingCreateSerializer,
    ActorSerializer,
    ActorListSerializer,
    ActorDetailSerializer,
    ActorImageSerializer,
    DirectorSerializer,
    DirectorListSerializer,
    DirectorDetailSerializer,
    DirectorImageSerializer,
    CategoryCreateSerializer,
    GenreCreateSerializer,
    MovieFramesSerializer,
    MovieFramesImageSerializer,
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
        if self.action == "upload_poster":
            return MoviePosterSerializer
        return super().get_serializer_class()

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-poster",
        permission_classes=[IsAdminUser],
    )
    def upload_poster(self, request, pk=None):
        """Endpoint for uploading poster to specific movie"""
        movie = self.get_object()
        serializer = self.get_serializer(movie, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        if self.action == "upload_image":
            return ActorImageSerializer
        return super().get_serializer_class()

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific actor"""
        actor = self.get_object()
        serializer = self.get_serializer(actor, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        if self.action == "upload_image":
            return DirectorImageSerializer
        return super().get_serializer_class()

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific director"""
        director = self.get_object()
        serializer = self.get_serializer(director, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def get_serializer_class(self):
        if self.action == "upload_image":
            return MovieFramesImageSerializer
        return super().get_serializer_class()

    @action(
        methods=["POST"],
        detail=False,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading images to movie frames"""
        movie_frame = self.get_object()
        serializer = self.get_serializer(movie_frame, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
