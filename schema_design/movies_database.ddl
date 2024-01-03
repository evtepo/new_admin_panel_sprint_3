CREATE SCHEMA IF NOT EXISTS content;

CREATE TYPE type_of_film_work AS ENUM ('movie', 'tv_show');

CREATE TYPE person_role AS ENUM ('actor', 'writer', 'director');

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL UNIQUE,
    description TEXT,
    creation_date DATE,
    rating FLOAT CHECK (rating >= 0 and rating <= 10),
    type type_of_film_work,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL UNIQUE,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role person_role,
    created timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid NOT NULL,
    film_work_id uuid NOT NULL,
    created timestamp with time zone
);

CREATE INDEX film_work_creation_date_idx ON content.film_work (creation_date);

CREATE INDEX film_work_title_rating_idx ON content.film_work (title, rating);

CREATE INDEX film_work_title_creation_date_idx ON content.film_work (title, creation_date);

CREATE UNIQUE INDEX film_work_person_idx ON content.person_film_work (film_work_id, person_id, role);

CREATE UNIQUE INDEX film_work_genre_idx ON content.genre_film_work (film_work_id, genre_id);
