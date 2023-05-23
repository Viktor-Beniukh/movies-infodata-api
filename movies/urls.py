from django.urls import path, include
from rest_framework import routers

from movies import views


app_name = "movies"


router = routers.DefaultRouter()
router.register("movies", views.MovieViewSet, basename="movie")
router.register("reviews", views.ReviewViewSet, basename="reviews")
router.register("ratings", views.AddStarRatingViewSet, basename="ratings")
router.register("actors", views.ActorViewSet, basename="actor")
router.register("directors", views.DirectorViewSet, basename="director")
router.register("categories", views.CategoryViewSet, basename="categories")
router.register("genres", views.GenreViewSet, basename="genres")
router.register(
    "movie-frames", views.MovieFramesViewSet, basename="movie-frames"
)

urlpatterns = [path("", include(router.urls))]
