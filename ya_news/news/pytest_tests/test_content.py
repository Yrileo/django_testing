from django.urls import reverse
from http import HTTPStatus
import pytest

from news.forms import CommentForm
from .utils import URL

pytestmark = pytest.mark.django_db
NEWS_COUNT_ON_HOME_PAGE = 10


def assert_sorted_by_created(objects):
    sorted_objects = sorted(objects, key=lambda x: x.created)
    assert list(objects) == sorted_objects


def test_anonymous_not_has_form(client, pk_news):
    name = URL['detail']
    url = reverse(name, args=[pk_news[0]])
    response = client.get(url)
    assert 'form' not in response.context


def test_user_has_form(admin_client, pk_news):
    name = URL['detail']
    url = reverse(name, args=[pk_news[0]])
    response = admin_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


def test_news_count_page(client, name):
    url = reverse(name)
    response = client.get(url)
    object_list = response.context['object_list']
    assert object_list.count() <= NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client):
    name = URL['home']
    url = reverse(name)
    response = client.get(url)
    object_list = response.context['object_list']
    assert_sorted_by_created(object_list)


def test_comment_order(client, pk_news):
    name = URL['detail']
    url = reverse(name, args=[pk_news[0]])
    response = client.get(url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert_sorted_by_created(all_comments)
