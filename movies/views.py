from rest_framework import generics

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


class MovieListView(generics.ListAPIView):
    serializer_class = MovieListSerializer

    def get_queryset(self):
        queryset = Movie.objects.filter(draft=False)
        return queryset


class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddStarRatingView(generics.CreateAPIView):
    serializer_class = RatingCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ActorsListView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer


class DirectorsListView(generics.ListAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorListSerializer


class DirectorDetailView(generics.RetrieveAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorDetailSerializer
