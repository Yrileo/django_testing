from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from .constants import Urls, UsrClient


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, parametrized_client, status_code',
    ((Urls.NEWS_HOME, UsrClient.ANONYMOUS, HTTPStatus.OK),
     (Urls.NEWS_DETAIL, UsrClient.ANONYMOUS, HTTPStatus.OK),
     (Urls.LOGIN, UsrClient.ANONYMOUS, HTTPStatus.OK),
     (Urls.LOGOUT, UsrClient.ANONYMOUS, HTTPStatus.OK),
     (Urls.SIGNUP, UsrClient.ANONYMOUS, HTTPStatus.OK),
     (Urls.NEWS_EDIT, UsrClient.AUTHOR, HTTPStatus.OK),
     (Urls.NEWS_DELETE, UsrClient.AUTHOR, HTTPStatus.OK),
     (Urls.NEWS_EDIT, UsrClient.READER, HTTPStatus.NOT_FOUND),
     (Urls.NEWS_DELETE, UsrClient.READER, HTTPStatus.NOT_FOUND),
     )
)
def test_pages_availability(url, parametrized_client, status_code):
    assert parametrized_client.get(url).status_code == status_code


@pytest.mark.parametrize(
    'url, expected_url',
    ((Urls.NEWS_EDIT, Urls.REDIRECT_EDIT),
     (Urls.NEWS_DELETE, Urls.REDIRECT_DELETE))
)
def test_redirect_to_login_page(client, url, expected_url):
    assertRedirects(client.get(url), expected_url)
