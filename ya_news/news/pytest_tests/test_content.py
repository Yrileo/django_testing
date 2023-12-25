from datetime import timedelta, datetime

import pytest

from django.shortcuts import reverse
from news.forms import CommentForm
from news.models import News, Comment

pytestmark = pytest.mark.django_db
NEWS_COUNT_ON_PAGE = 10


def test_news_count(client, url_home):
    response = client.get(url_home)
    object_list = response.context.get('object_list', None)
    assert object_list is not None
    news_count = len(object_list)
    assert news_count <= NEWS_COUNT_ON_PAGE


def test_news_order(client, url_home):
    start_date = datetime.today()

    for index in range(5):
        interval = timedelta(days=1)
        created_date = start_date - index * interval
        News.objects.create(
            title=f'Title {index}',
            text=f'Text {index}',
            date=created_date,
        )

    response = client.get(url_home)
    object_list = response.context.get('object_list', None)
    assert object_list is not None
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client):
    news = News.objects.create(
        title='Test News', text='Test Text', date=datetime.today()
    )

    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    comments_sorted = Comment.objects.order_by('created')
    all_dates_comments = [comment.created for comment in comments_sorted]
    all_dates = [comment.created for comment in all_comments]
    assert all_dates_comments == all_dates


def test_comment_form_availability_for_different_users(client, url_detail):
    response = client.get(url_detail)
    assert 'form' not in response.context


def test_for_author_in_form_there_commentform(admin_client, url_detail):
    response = admin_client.get(url_detail)
    assert ('form' in response.context) is True
    list_forms = response.context['form']
    assert isinstance(list_forms, CommentForm)
