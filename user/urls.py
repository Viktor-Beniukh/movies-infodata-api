from django.urls import path

from user.views import (
    CreateUserView,
    CreateTokenView,
    ManageUserView,
    CreateProfileView,
    UpdateProfileView,
)


app_name = "user"


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("token/", CreateTokenView.as_view(), name="token"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path(
        "profile/create/",
        CreateProfileView.as_view(),
        name="profile-create"
    ),
    path(
        "profile/<int:pk>/update/",
        UpdateProfileView.as_view(),
        name="profile-update"
    ),
]
