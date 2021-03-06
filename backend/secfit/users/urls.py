from django.urls import path, include, re_path
from users import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("reset_password/<str:uid>/<str:token>/", views.UserResetPasswordView.as_view(), name="reset_password"),
    path("activate/<str:uid>/<str:token>/", views.UserActivationView.as_view(), name="activate"),
    path("api/users/", views.UserList.as_view(), name="user-list"),
    path("api/users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
    path("api/users/<str:username>/", views.UserDetail.as_view(), name="user-detail"),
    path("api/offers/", views.OfferList.as_view(), name="offer-list"),
    path("api/offers/<int:pk>/", views.OfferDetail.as_view(), name="offer-detail"),
    path(
        "api/athlete-files/", views.AthleteFileList.as_view(), name="athlete-file-list"
    ),
    path(
        "api/athlete-files/<int:pk>/",
        views.AthleteFileDetail.as_view(),
        name="athletefile-detail",
    ),
    re_path(
        r'^totp/create/$', 
        views.TOTPCreateView.as_view(), 
        name='totp-create'
        ), # create view for "creating" totp
    re_path(
        r'^totp/login/(?P<token>[0-9]{6})/$', 
        views.TOTPVerifyView.as_view(), 
        name='totp-login'
        ), # Create view for totp login
]

