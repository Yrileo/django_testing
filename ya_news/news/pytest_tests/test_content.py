import pytest

from news.forms import CommentForm

pytestmark = pytest.mark.django_db
NEWS_COUNT_ON_PAGE = 10


def test_news_count(client, url_home):
    response = client.get(url_home)
    object_list = response.context.get('object_list', [])
    print(f"Number of news articles: {len(object_list)}")
    print(f"News articles: {object_list}")
    news_count = len(object_list)
    assert news_count <= NEWS_COUNT_ON_PAGE


def test_news_order(client, url_home):
    response = client.get(url_home)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, url_detail):
    response = client.get(url_detail)
    list_comments = response.context['news'].comment_set.all()
    all_dates = [comment.created for comment in list_comments]
    sorted_dates = sorted(all_dates)
    assert all_dates == sorted_dates


def test_comment_form_availability_for_different_users(client, url_detail):
    response = client.get(url_detail)
    assert ('form' in response.context) is False


def test_for_author_in_form_there_commentform(admin_client, url_detail):
    response = admin_client.get(url_detail)
    assert ('form' in response.context) is True
    list_forms = response.context['form']
    assert isinstance(list_forms, CommentForm)
