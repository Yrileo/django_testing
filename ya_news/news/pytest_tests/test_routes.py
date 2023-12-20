from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from .utils import ADMIN, AUTHOR, CLIENT, PK, URL


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, pk, parametrized_client, expected_status',
    [
        (URL['detail'], PK, CLIENT, HTTPStatus.OK),
        (URL['edit'], PK, AUTHOR, HTTPStatus.OK),
        (URL['delete'], PK, AUTHOR, HTTPStatus.OK),
        (URL['edit'], PK, ADMIN, HTTPStatus.NOT_FOUND),
        (URL['delete'], PK, ADMIN, HTTPStatus.NOT_FOUND),
        (URL['home'], None, CLIENT, HTTPStatus.OK),
        (URL['login'], None, CLIENT, HTTPStatus.OK),
        (URL['logout'], None, CLIENT, HTTPStatus.OK),
        (URL['signup'], None, CLIENT, HTTPStatus.OK),
    ]
)
def test_page_availability(
    # не понимаю почему при удаление comment все ломается
    name, pk, parametrized_client, expected_status, comment
):
    url = reverse(name, args=pk) if pk else reverse(name)

    if name in [URL['edit'], URL['delete']] and not pk:
        login_url = reverse(URL["login"])
        expected_url = f'{login_url}?next={url}'
        response = parametrized_client.get(url)
        assertRedirects(response, expected_url)
    else:
        response = parametrized_client.get(url)
        assert response.status_code == expected_status
