from django.urls import path

from .views import MoviesListApi, SingleMovieApi


urlpatterns = [
    path("movies/", MoviesListApi.as_view()),
    path("movies/<uuid:pk>/", SingleMovieApi.as_view()),
]
