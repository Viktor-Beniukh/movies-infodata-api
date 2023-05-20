from rest_framework import routers

from movies import views


app_name = "movies"


router = routers.DefaultRouter()
router.register("movies", views.MovieViewSet, basename="movies")
router.register("reviews", views.ReviewViewSet, basename="reviews")
router.register("ratings", views.AddStarRatingViewSet, basename="ratings")
router.register("actors", views.ActorViewSet, basename="actors")
router.register("directors", views.DirectorViewSet, basename="directors")


urlpatterns = router.urls
