from django.conf import settings
from django.urls import reverse
from news.forms import CommentForm

import pytest

from .utils import PK, URL


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, pk', ((URL['detail'], PK),))
def test_anonymous_not_has_form(client, name, pk):
    url = reverse(name, args=pk)
    response = client.get(url)
    assert 'form' not in response.context


@pytest.mark.parametrize('name, pk', ((URL['detail'], PK),))
def test_user_has_form(admin_client, name, pk, news):
    url = reverse(name, args=pk)
    response = admin_client.get(url)
    assert 'form' in response.context
    assert (isinstance(response.context['form'], CommentForm))


@pytest.mark.django_db
@pytest.mark.parametrize('name', (URL['home'],),)
def test_news_count_page(client, name, news_list):
    url = reverse(name)
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert object_list.count() == settings.NEWS_COUNT_ON_HOME_PAGE
    assert all_dates == sorted_dates


@pytest.mark.django_db
@pytest.mark.parametrize('name, pk', ((URL['detail'], PK),))
def test_comment_order(client, news, name, pk):
    url = reverse(name, args=pk)
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert list(all_comments) == sorted(all_comments, key=lambda x: x.created)
