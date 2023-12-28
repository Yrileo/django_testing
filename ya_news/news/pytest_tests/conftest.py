import pytest

from django.conf import settings
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Author')


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Reader')


@pytest.fixture
def author_client(author):
    author_client = Client()
    author_client.force_login(author)
    return author_client


@pytest.fixture
def reader_client(reader):
    reader_client = Client()
    reader_client.force_login(reader)
    return reader_client


@pytest.fixture
def news():
    return News.objects.create(
        title='Test News',
        text='Some text',
    )


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Test Comment',
    )


@pytest.fixture
def bulk_news():
    today = timezone.now()
    return News.objects.bulk_create(
        News(
            title=f'Новость #{index}',
            text=f'Simple text #{index}.',
            date=today - timezone.timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def bulk_comments(news, author):
    today = timezone.now()
    for index in range(3):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Comment text #{index}'
        )
        comment.created = today - timezone.timedelta(days=index)
        comment.save()


@pytest.fixture
def news_home_url():
    return reverse('news:home')


@pytest.fixture
def news_detail_url(news):
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def news_delete_url(comment):
    return reverse('news:delete', args=(comment.pk,))


@pytest.fixture
def news_edit_url(comment):
    return reverse('news:edit', args=(comment.pk,))


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture()
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture
def to_news_edit_url_after_login(login_url, news_edit_url):
    return f'{login_url}?next={news_edit_url}'


@pytest.fixture
def to_news_delete_url_after_login(login_url, news_delete_url):
    return f'{login_url}?next={news_delete_url}'


@pytest.fixture
def to_news_detail_url_after_login(login_url, news_detail_url):
    return f'{login_url}?next={news_detail_url}'
