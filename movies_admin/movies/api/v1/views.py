from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from ...models import Filmwork, PersonFilmwork


class MoviesApiMixin:
    """
    Mixin Класс с методами для получения
    queryset и отправки данных в json формате.
    """

    http_method_names = ("get",)
    model = Filmwork

    def get_queryset(self):
        queryset = (
            self.model.objects.all()
            .values()
            .annotate(
                genres=ArrayAgg(
                    "genres__name",
                    distinct=True,
                ),
                actors=ArrayAgg(
                    "persons__full_name",
                    filter=Q(personfilmwork__role=PersonFilmwork.Roles.ACTOR),
                    distinct=True,
                ),
                directors=ArrayAgg(
                    "persons__full_name",
                    filter=Q(personfilmwork__role=PersonFilmwork.Roles.DIRECTOR),
                    distinct=True,
                ),
                writers=ArrayAgg(
                    "persons__full_name",
                    filter=Q(personfilmwork__role=PersonFilmwork.Roles.WRITER),
                    distinct=True,
                ),
            )
            .values(
                "id",
                "title",
                "description",
                "creation_date",
                "rating",
                "type",
                "genres",
                "actors",
                "directors",
                "writers",
            )
        )

        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    """
    View Класс для получения всех кинопроизведений.
    """

    paginate_by = 50

    def get_context_data(self, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, self.paginate_by
        )

        if is_paginated:
            prev_page = page.number - 1 if page.number - 1 > 0 else None
            next_page = (
                page.number + 1 if page.number + 1 <= paginator.num_pages else None
            )
        else:
            prev_page, next_page = 1, 1

        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": prev_page,
            "next": next_page,
            "results": list(queryset),
        }

        return context


class SingleMovieApi(MoviesApiMixin, BaseDetailView):
    """
    View Класс для получения одного кинопроизведения.
    """

    def get_object(self):
        uuid = self.kwargs.get(self.pk_url_kwarg)
        queryset = self.get_queryset()

        queryset = dict(queryset.get(id=uuid))

        return queryset

    def get_context_data(self, **kwargs):
        return self.get_object()
