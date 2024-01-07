from typing import List, Dict, Any, Union


def get_valid_data(
    id: str,
    rating: float,
    genre: List[str],
    title: str,
    description: str,
    persons: List[Union[Dict[str, Any], None]],
    modified: str,
) -> Dict[str, Any]:
    """
    Функция для преобразования данных пригодных для Elasticsearch
    """

    people = {
        "writer": [],
        "actor": [],
        "director": [],
    }

    for person in persons:
        people.setdefault(person.get("person_role"), []).append(
            {
                "id": person.get("person_id"),
                "name": person.get("person_name"),
            }
        )

    return {
        "id": id,
        "imdb_rating": rating,
        "genre": list(genre),
        "title": title,
        "description": description,
        "director": list(map(lambda x: x.get("name"), people.get("director"))),
        "actors_names": list(map(lambda x: x.get("name"), people.get("actor"))),
        "writers_names": list(map(lambda x: x.get("name"), people.get("writer"))),
        "actors": list(people.get("actor")),
        "writers": list(people.get("writer")),
    }


def get_modified_field(*args):
    """Функция для получения modified последнего объекта"""

    return args[-1]
