from django.contrib import admin

from django.utils.translation import gettext_lazy as _

from .models import Genre, Filmwork, Person, GenreFilmwork, PersonFilmwork


class InlineMixin(admin.TabularInline):
    extra = 0

    class Meta:
        abstract = True


class AdminSettingsMixin(admin.ModelAdmin):
    show_full_result_count = False

    class Meta:
        abstract = True


@admin.register(Genre)
class GenreAdmin(AdminSettingsMixin):
    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )


@admin.register(Person)
class PersonAdmin(AdminSettingsMixin):
    list_display = (
        "full_name",
    )

    search_fields = (
        "full_name",
    )


class GenreFilmworkInline(InlineMixin):
    model = GenreFilmwork
    autocomplete_fields = ("genre",)


class PersonFilmworkInline(InlineMixin):
    model = PersonFilmwork
    autocomplete_fields = ("person",)


@admin.register(Filmwork)
class FilmworkAdmin(AdminSettingsMixin):
    inlines = (
        GenreFilmworkInline,
        PersonFilmworkInline,
    )

    list_display = (
        "title",
        "get_genres",
        "get_actors",
        "get_directors",
        "get_writers",
        "creation_date",
        "rating",
        "type",
    )

    list_filter = (
        "type",
        "genres",
        "persons",
    )

    search_fields = (
        "title",
        "description",
    )

    list_prefetch_related = ("genres", "persons", "personfilmwork_set__person")

    def get_queryset(self, request):
        queryset = (
            super().get_queryset(request).prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return [genre.name for genre in obj.genres.all()]

    def get_member(self, obj, role):
        members = []
        for person_filmwork in obj.personfilmwork_set.all():
            if person_filmwork.role == role:
                members.append(person_filmwork.person.full_name)

        return members

    def get_actors(self, obj):
        return self.get_member(obj, "actor")

    def get_directors(self, obj):
        return self.get_member(obj, "director")

    def get_writers(self, obj):
        return self.get_member(obj, "writer")

    get_genres.short_description = _("genre")

    get_actors.short_description = _("actor")

    get_directors.short_description = _("director")

    get_writers.short_description = _("writer")
