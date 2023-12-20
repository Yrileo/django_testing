from http import HTTPStatus
import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from .utils import CLIENT, URL


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, parametrized_client, expected_status',
    (
        (URL['home'], CLIENT, HTTPStatus.OK),
        (URL['login'], CLIENT, HTTPStatus.OK),
        (URL['logout'], CLIENT, HTTPStatus.OK),
        (URL['signup'], CLIENT, HTTPStatus.OK),
        (URL['edit'], CLIENT, HTTPStatus.FOUND),
        (URL['delete'], CLIENT, HTTPStatus.FOUND),
    )
)
def test_page_availability_for_users(
    name, parametrized_client, expected_status
):
    url = reverse(name)
    response = parametrized_client.get(url)

    if expected_status == HTTPStatus.FOUND:
        login_url = reverse(URL["login"])
        expected_url = f'{login_url}?next={url}'
        assertRedirects(response, expected_url)
    else:
        assert response.status_code == expected_status
