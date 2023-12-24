from http import HTTPStatus
from random import choice

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


def test_author_can_edit_comment(
        author_client, form_data, comment, news, url_detail, url_edit, author
):
    set_comments_old = set(Comment.objects.all())
    count_old = Comment.objects.count()
    response = author_client.post(url_edit, data=form_data)
    expected_url = f'{url_detail}#comments'
    assertRedirects(response, expected_url)
    set_comments_new = set(Comment.objects.all())
    differences = len(set_comments_old.difference(set_comments_new))
    assert differences == 0
    count_new = Comment.objects.count()
    comment = set_comments_new.pop()
    assert comment.text == form_data['text']
    assert comment.author == author
    assert comment.news == news
    assert count_old == count_new


def test_other_user_cant_edit_comment(
        admin_client, form_data, comment, url_edit, author, news
):
    set_comments_old = set(Comment.objects.all())
    count_old = Comment.objects.count()
    response = admin_client.post(url_edit, form_data)
    old_com = comment.text
    assert response.status_code == HTTPStatus.NOT_FOUND
    set_comments_new = set(Comment.objects.all())
    count_new = Comment.objects.count()
    differences = len(set_comments_old.difference(set_comments_new))
    assert differences == 0
    comment = set_comments_new.pop()
    assert comment.text == old_com
    assert comment.author == author
    assert comment.news == news
    assert count_old == count_new


def test_author_can_delete_comment(
        author_client, url_delete, url_detail
):
    count_old = Comment.objects.count()
    response = author_client.post(url_delete)
    expected_url = f'{url_detail}#comments'
    assertRedirects(response, expected_url)
    count_new = Comment.objects.count()
    assert count_old - 1 == count_new


def test_other_user_cant_delete_comment(
        admin_client, url_delete
):
    count_old = Comment.objects.count()
    response = admin_client.post(url_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    count_new = Comment.objects.count()
    assert count_old == count_new


def test_user_can_create_comment(
    author_client, news, form_data, url_detail, author
):
    set_comments_old = set(Comment.objects.all())
    count_old = Comment.objects.count()
    response = author_client.post(url_detail, data=form_data)
    expected_url = f'{url_detail}#comments'
    assertRedirects(response, expected_url)
    set_comments_new = set(Comment.objects.all())
    differences = len(set_comments_new.difference(set_comments_old))
    assert differences == 1
    comment = set_comments_new.pop()
    count_new = Comment.objects.count()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author
    assert count_old + 1 == count_new


def test_other_user_cant_create_comment(
        client, form_data, url_detail, login_url
):
    count_old = Comment.objects.count()
    response = client.post(url_detail, data=form_data)
    expected_url = f'{login_url}?next={url_detail}'
    assertRedirects(response, expected_url)
    count_new = Comment.objects.count()
    assert count_old == count_new


def test_user_cant_use_bad_words(admin_client, url_detail):
    count_old = Comment.objects.count()
    bad_words_data = {'text': f'Mr Petrov {choice(BAD_WORDS)}!'}
    response = admin_client.post(url_detail, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    count_new = Comment.objects.count()
    assert count_old == count_new
