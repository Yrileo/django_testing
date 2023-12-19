from django.urls import reverse

import pytest

from news.forms import CommentForm
from .utils import PK, URL

pytestmark = pytest.mark.django_db


def assert_sorted_by_created(objects):
    sorted_objects = sorted(objects, key=lambda x: x.created)
    assert list(objects) == sorted_objects


@pytest.mark.parametrize('name, pk', ((URL['detail'], PK),))
def test_anonymous_not_has_form(client, name, pk):
    url = reverse(name, args=pk)
    response = client.get(url)
    assert 'form' not in response.context


@pytest.mark.parametrize('name, pk', ((URL['detail'], PK),))
def test_user_has_form(admin_client, name, pk):
    url = reverse(name, args=pk)
    response = admin_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


@pytest.mark.parametrize('name', (URL['home'],),)
def test_news_count_page(client, name):
    url = reverse(name)
    response = client.get(url)
    object_list = response.context['object_list']
    assert object_list.count() <= 10


@pytest.mark.parametrize('name, pk', ((URL['detail'], PK),))
def test_comment_order(client, news, name, pk):
    url = reverse(name, args=pk)
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert_sorted_by_created(all_comments)
