import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDMixin(models.Model):
    """
    Класс Mixin для добавления id в модели.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampMixin(models.Model):
    """
    Класс Mixin для добавления дат создания и редактирования в моделях.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampMixin):
    """
    Модель для описания жанров кинопроизведений.
    """
    name = models.CharField(_("name"), max_length=255, unique=True)
    description = models.TextField(_("description"), blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _("genre")
        verbose_name_plural = _("genres")


class Person(UUIDMixin, TimeStampMixin):
    """
    Модель для описания участников кинопроизведений.
    """
    full_name = models.CharField(_("full_name"), max_length=255, unique=True)

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _("participant")
        verbose_name_plural = _("participants")


class Filmwork(UUIDMixin, TimeStampMixin):
    """
    Модель для описания кинопроизведений.
    """
    class TypeOfMovies(models.TextChoices):
        MOVIE = "movie", "Movie"
        TV_SHOW = "tv_show", "TV_show"

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)
    creation_date = models.DateField(_("date of creation"))
    rating = models.FloatField(
        _("rating"),
        blank=True,
        validators=(
            MinValueValidator(0),
            MaxValueValidator(10),
        )
    )
    type = models.TextField(_("type"), choices=TypeOfMovies.choices)
    genres = models.ManyToManyField(
        Genre,
        through="GenreFilmwork",
        verbose_name=_("genre"),
    )
    persons = models.ManyToManyField(
        Person,
        through="PersonFilmwork",
        verbose_name=_("person"),
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _("film work")
        verbose_name_plural = _("film works")
        indexes = (
            models.Index(
                fields=("creation_date",),
                name="creation_date_idx",
            ),
            models.Index(
                fields=("title", "rating"),
                name="title_rating_idx",
            ),
            models.Index(
                fields=("title", "creation_date"),
                name="title_creation_date_idx",
            ),
        )


class GenreFilmwork(UUIDMixin):
    """
    Модель для связи между Genre и Filmwork.
    """
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name=_("genre")
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return ""

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _("film genre")
        verbose_name_plural = _("film genres")
        constraints = (
            models.UniqueConstraint(
                fields=("film_work", "genre"),
                name="film_work_genre_idx",
            ),
        )


class PersonFilmwork(UUIDMixin):
    """
    Модель для связи между Person и Filmwork.
    """
    class Roles(models.TextChoices):
        ACTOR = "actor", "Actor"
        WRITER = "writer", "Writer"
        DIRECTOR = "director", "Director"
        
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name=_("person")
    )
    role = models.TextField(_("role"), choices=Roles.choices)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return ""

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _("film participant")
        verbose_name_plural = _("film participants")
        constraints = (
            models.UniqueConstraint(
                fields=("film_work", "person", "role"),
                name="film_work_person_idx",
            ),
        )
