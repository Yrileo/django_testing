from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture

pytestmark = pytest.mark.django_db

DETAIL = lazy_fixture('url_detail')
HOME = lazy_fixture('url_home')
LOGIN = lazy_fixture('login_url')
LOGOUT = lazy_fixture('logout_url')
SIGNUP = lazy_fixture('signup_url')
EDIT = lazy_fixture('url_edit')
DELETE = lazy_fixture('url_delete')
CLIENT = pytest.lazy_fixture('client')
AUTHOR = pytest.lazy_fixture('author_client')
ADMIN = pytest.lazy_fixture('admin_client')


@pytest.mark.parametrize(
    'url, clients, status', (
        (DETAIL, CLIENT, HTTPStatus.OK),
        (HOME, CLIENT, HTTPStatus.OK),
        (LOGIN, CLIENT, HTTPStatus.OK),
        (LOGOUT, CLIENT, HTTPStatus.OK),
        (SIGNUP, CLIENT, HTTPStatus.OK),
        (EDIT, AUTHOR, HTTPStatus.OK),
        (EDIT, ADMIN, HTTPStatus.NOT_FOUND),
        (DELETE, AUTHOR, HTTPStatus.OK),
        (DELETE, ADMIN, HTTPStatus.NOT_FOUND))
)
def test_pages_availability_for_certain_user(
    url, clients, status
):
    response = clients.get(url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'url',
    (DELETE, EDIT),
)
def test_redirects(client, url, login_url):
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
