from http import HTTPStatus

import pytest

from django.urls import reverse
from pytest_django.asserts import assertRedirects
from .utils import ADMIN, AUTHOR, CLIENT, PK, URL


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, pk, parametrized_client, expected_status',
    (
        (URL['detail'], PK, CLIENT, HTTPStatus.OK),
        (URL['edit'], PK, AUTHOR, HTTPStatus.OK),
        (URL['delete'], PK, AUTHOR, HTTPStatus.OK),
        (URL['edit'], PK, ADMIN, HTTPStatus.NOT_FOUND),
        (URL['delete'], PK, ADMIN, HTTPStatus.NOT_FOUND),
    )
)
def test_page_availability_for_another_user(
    name, pk, parametrized_client, expected_status, comment
):
    url = reverse(name, args=pk)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, parametrized_client, expected_status',
    (
        (URL['home'], CLIENT, HTTPStatus.OK),
        (URL['login'], CLIENT, HTTPStatus.OK),
        (URL['logout'], CLIENT, HTTPStatus.OK),
        (URL['signup'], CLIENT, HTTPStatus.OK),
    )
)
def test_page_availability_for_anonymous_user(
    name, parametrized_client, expected_status
):
    url = reverse(name)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, pk',
    (
        (URL['edit'], PK),
        (URL['delete'], PK),
    ),
)
def test_redirect_anonymous_user(client, name, pk):
    url = reverse(name, args=pk)
    login_url = reverse(URL["login"])
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
