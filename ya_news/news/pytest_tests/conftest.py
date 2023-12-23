from datetime import timedelta, datetime

from django.conf import settings
from django.test import Client

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


# умирает у меня все без этого, никак не могу победить
@pytest.fixture
def pk_news(news):
    return news.pk,


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def eleven_news():
    today = datetime.today()
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        date = today - timedelta(days=index)
        News.objects.create(
            title=f'Текст новости {index}',
            text='Заголовок новости',
            date=date,
        )
    return News.objects.all().order_by('-date')


@pytest.fixture
def comments_list(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment
