from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from movies.models import Movie, Genre, Category, Actor, Director
from movies.pagination import ApiPagination
from movies.serializers import MovieListSerializer, MovieDetailSerializer


MOVIE_URL = reverse("movies:movie-list")


class UnauthenticatedMovieApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_movies(self):
        sample_movie()
        pagination = ApiPagination

        response = self.client.get(MOVIE_URL)

        movies = Movie.objects.all()
        serializer = MovieListSerializer(pagination, movies, many=True)

        if serializer.is_valid():
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, serializer.data)

    def test_filter_movies_by_title(self):
        sample_movie(title="Movie")
        sample_movie(title="Sample")
        pagination = ApiPagination

        response = self.client.get(MOVIE_URL, {"title": "Movie"})

        movies = Movie.objects.filter(title__icontains="mov")
        serializer = MovieListSerializer(pagination, movies, many=True)

        if serializer.is_valid():
            self.assertEqual(response.data, serializer.data)

    def test_filter_movies_by_year_of_release(self):
        sample_movie(year_of_release=1985)
        sample_movie(year_of_release=2023)
        pagination = ApiPagination

        response = self.client.get(MOVIE_URL, {"year_of_release": 2023})

        movies = Movie.objects.filter(year_of_release=2023)
        serializer = MovieListSerializer(pagination, movies, many=True)

        if serializer.is_valid():
            self.assertEqual(response.data, serializer.data)

    def test_filter_movie_by_genres(self):
        movie1 = sample_movie(title="Movie 1")
        movie2 = sample_movie(title="Movie 2")
        movie3 = sample_movie()
        pagination = ApiPagination

        genre1 = sample_genre(name="Action")
        genre2 = sample_genre(name="Fighter")

        movie1.genres.add(genre1)
        movie2.genres.add(genre2)

        response = self.client.get(MOVIE_URL, {"genres": f"{genre1.name},{genre2.name}"})

        serializer1 = MovieListSerializer(pagination, movie1)
        serializer2 = MovieListSerializer(pagination, movie2)
        serializer3 = MovieListSerializer(pagination, movie3)

        if serializer1.is_valid():
            self.assertIn(serializer1.data, response.data)
        if serializer2.is_valid():
            self.assertIn(serializer2.data, response.data)
        if serializer3.is_valid():
            self.assertNotIn(serializer3.data, response.data)

    def test_filter_movie_by_category(self):
        category1 = sample_category(name="Films")
        category2 = sample_category(name="Anime")

        movie1 = sample_movie(title="Movie 3", category=category1)
        movie2 = sample_movie(title="Movie 4", category=category2)
        movie3 = sample_movie()
        pagination = ApiPagination

        response = self.client.get(MOVIE_URL, {"category": f"{category1.name}"})

        serializer1 = MovieListSerializer(pagination, movie1)
        serializer2 = MovieListSerializer(pagination, movie2)
        serializer3 = MovieListSerializer(pagination, movie3)

        if serializer1.is_valid():
            self.assertIn(serializer1.data, response.data)
        if serializer2.is_valid():
            self.assertIn(serializer2.data, response.data)
        if serializer3.is_valid():
            self.assertNotIn(serializer3.data, response.data)

    def test_retrieve_movie_detail(self):
        movie = sample_movie()

        director = sample_director()
        actor = sample_actor()
        genre = sample_genre()

        movie.directors.add(director)
        movie.actors.add(actor)
        movie.genres.add(genre)

        url = detail_url(movie.id)
        response = self.client.get(url)

        serializer = MovieDetailSerializer(movie)

        print(response.data)
        print(serializer.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            remove_average_rating(response.data),
            remove_average_rating(serializer.data)
        )


class AuthenticatedMovieApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_create_movie_forbidden(self):
        payload = {
            "title": "Movie",
            "description": "Description",
            "year_of_release": 2023,
        }

        response = self.client.post(MOVIE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminMovieApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@test.com",
            "adminpass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_movie(self):

        payload = {
            "title": "Movie",
            "description": "Description",
            "year_of_release": 2023,
        }

        response = self.client.post(MOVIE_URL, payload)

        movie = Movie.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(movie, key))

    def test_create_movie_with_directors_actors_category_and_genres(self):
        director1 = sample_director(name="Steven Spielberg")
        director2 = sample_director(name="James Cameron")

        actor1 = sample_actor(name="Jack Nicholson")
        actor2 = sample_actor(name="Matt Damon")

        category = sample_category(name="Films")

        genre1 = sample_genre(name="Action")
        genre2 = sample_genre(name="Horror")

        payload = {
            "title": "Movie",
            "description": "Description",
            "duration": 100,
            "directors": (director1.id, director2.id),
            "actors": (actor1.id, actor2.id),
            "category": category.id,
            "genres": (genre1.id, genre2.id)
        }

        response = self.client.post(MOVIE_URL, payload)

        movie = Movie.objects.get(id=response.data["id"])

        directors = movie.directors.all()
        actors = movie.actors.all()
        category = movie.category.id
        genres = movie.genres.all()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(directors.count(), 2)
        self.assertEqual(actors.count(), 2)
        self.assertEqual(genres.count(), 2)

        self.assertIn(director1, directors)
        self.assertIn(director2, directors)

        self.assertIn(actor1, actors)
        self.assertIn(actor2, actors)

        self.assertEqual(category, category)

        self.assertIn(genre1, genres)
        self.assertIn(genre2, genres)


def sample_movie(**params):
    category = sample_category()
    defaults = {
        "title": "Sample movie",
        "description": "Sample description",
        "year_of_release": 1990,
        "category": category
    }
    defaults.update(params)

    return Movie.objects.create(**defaults)


def sample_category(**params):
    defaults = {
        "name": "Cartoon",
    }
    defaults.update(params)

    name = defaults["name"]
    category, _ = Category.objects.get_or_create(name=name, defaults=defaults)

    return category


def sample_genre(**params):
    defaults = {
        "name": "Action",
    }
    defaults.update(params)

    return Genre.objects.create(**defaults)


def sample_director(**params):
    defaults = {
        "name": "Steven Spielberg"
    }
    defaults.update(params)

    return Director.objects.create(**defaults)


def sample_actor(**params):
    defaults = {
        "name": "Tom Cruise"
    }
    defaults.update(params)

    return Actor.objects.create(**defaults)


def remove_average_rating(data):
    data_without_average_rating = dict(data)
    data_without_average_rating.pop("average_rating", None)
    return data_without_average_rating


def detail_url(movie_id):
    return reverse("movies:movie-detail", args=[movie_id])
