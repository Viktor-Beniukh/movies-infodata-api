from django.urls import path

from movies import views

app_name = "movies"


urlpatterns = [
    path(
        "movie/",
        views.MovieListView.as_view(),
        name="movie-list"
    ),
    path(
        "movie/<int:pk>/",
        views.MovieDetailView.as_view(),
        name="movie-detail"
    ),
    path(
        "review/",
        views.ReviewCreateView.as_view(),
        name="review-create"
    ),
    path(
        "rating/",
        views.AddStarRatingView.as_view(),
        name="rating-create"
    ),
    path(
        "actors/",
        views.ActorsListView.as_view(),
        name="actors-list"
    ),
    path(
        "actors/<int:pk>/",
        views.ActorDetailView.as_view(),
        name="actor-detail"
    ),
    path(
        "directors/",
        views.DirectorsListView.as_view(),
        name="directors-list"
    ),
    path(
        "directors/<int:pk>/",
        views.DirectorDetailView.as_view(),
        name="director-detail"
    ),
]
