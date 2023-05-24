from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from user.views import (
    CreateUserView,
    ManageUserView,
    CreateProfileView,
    UpdateProfileView,
)


app_name = "user"


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path(
        "me/profile-create/",
        CreateProfileView.as_view(),
        name="profile-create"
    ),
    path(
        "me/<int:pk>/profile-update/",
        UpdateProfileView.as_view(),
        name="profile-update"
    ),
]
