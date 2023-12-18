from http import HTTPStatus

import pytest

from django.urls import reverse
from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from pytest_django.asserts import assertFormError, assertRedirects
from .utils import PK, URL, FORM_DATA


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, pk, form_data',
    (
        (URL['detail'], PK, FORM_DATA),
    )
)
def test_anonymous_user_cant_create_comment(client, name, pk, news, form_data):
    expected_comment_count = Comment.objects.count()
    url = reverse(name, args=pk)
    client.post(url, form_data)
    comment_count = Comment.objects.count()
    assert comment_count == expected_comment_count


@pytest.mark.parametrize('name, pk, form_data', (
    (URL['detail'], PK, FORM_DATA),
))
def test_user_can_create_comment(author_client, news, name, pk, form_data):
    expected_comment_count = Comment.objects.count() + 1
    url = reverse(name, args=pk)
    response = author_client.post(url, form_data)
    comment_count = Comment.objects.count()
    assert comment_count == expected_comment_count
    comment = Comment.objects.last()
    assertRedirects(response, f'{url}#comments')
    assert comment.text == form_data['text']


@pytest.mark.parametrize('name, name_news, pk', (
    (URL['delete'], URL['detail'], PK),
))
def test_author_can_delete_commet(
        author_client, news, name, name_news, pk, comment):
    expected_comment_count = Comment.objects.count() - 1
    url = reverse(name, args=pk)
    response = author_client.delete(url)
    comment_count = Comment.objects.count()
    url_redirect = reverse(name_news, args=pk)
    assertRedirects(response, f'{url_redirect}#comments')
    assert expected_comment_count == comment_count


@pytest.mark.parametrize('name, pk', ((URL['delete'], PK),))
def test_user_cant_delete_comment_of_another_user(
    admin_client, name, pk, comment
):
    expected_comment_count = Comment.objects.count()
    url = reverse(name, args=pk)
    response = admin_client.delete(url)
    comment_count = Comment.objects.count()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert expected_comment_count == comment_count


@pytest.mark.parametrize('name, name_news, pk, form_data', (
    (URL['edit'], URL['detail'], PK, FORM_DATA),
))
def test_author_can_edit_comment(
    author_client, comment, form_data, name, name_news, pk
):
    NEW_COMMENT_TEXT = 'Новый комментарий'
    url = reverse(name, args=pk)
    response = author_client.post(url, data=form_data)
    url_redirect = reverse(name_news, args=pk)
    assertRedirects(response, f'{url_redirect}#comments')
    comment.refresh_from_db()
    assert comment.text == NEW_COMMENT_TEXT


@pytest.mark.parametrize('name, pk, form_data', (
    (URL['edit'], PK, FORM_DATA),
))
def test_user_cant_edit_comment_of_another_user(
    admin_client, comment, name, pk, form_data
):
    url = reverse(name, args=pk)
    response = admin_client.post(url, data=form_data)
    comment.refresh_from_db()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment.text == comment.text


@pytest.mark.parametrize('name, pk', (
    (URL['detail'], PK),
))
@pytest.mark.parametrize('word', BAD_WORDS)
def test_user_cant_use_bad_words(author_client, news, name, pk, word):
    excepected_comment_count = Comment.objects.count()
    bad_words_data = {'text': f'Какой-то текст, {word}, еще текст'}
    url = reverse(name, args=pk)
    response = author_client.post(url, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    comment_count = Comment.objects.count()
    assert excepected_comment_count == comment_count
