from datetime import datetime, timedelta
import random

import pytest

from django.urls import reverse
from news.models import News, Comment

FORM_DATA = {
    'text': 'Новый текст'
}
URL_HOME = reverse('news:home')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст'
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def form_data():
    return FORM_DATA


@pytest.fixture
def make_many_news():
    start_date = datetime.today()

    for index in range(author, news, num_comments=2):
        interval = timedelta(days=1)
        created_date = start_date - index * interval
        Comment.objects.create(
            news=news,
            author=author,
            text=f'Text {index}',
            created=created_date,
        )


@pytest.fixture
def make_comments(author, news, num_comments=2):
    for index in range(num_comments):
        created_date = datetime.today() - timedelta(days=random.randint(1, 10))
        Comment.objects.create(
            news=news,
            author=author,
            text=f'Text {index}',
            created=created_date,
        )


@pytest.fixture
def url_detail(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def url_edit(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def url_delete(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def url_home():
    return URL_HOME


@pytest.fixture
def login_url():
    return LOGIN_URL


@pytest.fixture
def logout_url():
    return LOGOUT_URL


@pytest.fixture
def signup_url():
    return SIGNUP_URL
