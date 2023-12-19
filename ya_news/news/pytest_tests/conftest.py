from datetime import timedelta

from django.conf import settings
from django.test import Client
from django.utils import timezone

import pytest

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок новости',
        text='Текст новости'
    )


@pytest.fixture
def pk_news(news):
    return (news.pk,)


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def news_list():
    today = timezone.now()
    return News.objects.bulk_create(
        News(
            text=f'Текст новости {index}',
            title=f'Заголовок новости {index}',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ).order_by('-date')


@pytest.fixture
def comments_list(author, news):
    today = timezone.now()
    return [
        Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст комментария {index}',
            created=today + timedelta(days=index)
        )
        for index in range(3)
    ].order_by('-created')
