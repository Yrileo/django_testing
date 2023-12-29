from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


pytestmark = pytest.mark.django_db

NEW_TEXT_FOR_COMMENTS = dict(text='Comment!')


def test_reader_cant_edit_authors_comment(
        comment, reader_client, comment_edit_url
):
    assert reader_client.post(
        comment_edit_url,
        data=NEW_TEXT_FOR_COMMENTS
    ).status_code == HTTPStatus.NOT_FOUND
    comment_after = Comment.objects.get(pk=comment.pk)
    assert comment_after.text == comment.text
    assert comment_after.news == comment.news
    assert comment_after.author == comment.author


def test_delete_comment_by_author(author_client, comment_delete_url):
    comment = Comment.objects.first()
    response = author_client.post(comment_delete_url)
    assert response.status_code == HTTPStatus.FOUND
    with pytest.raises(Comment.DoesNotExist):
        Comment.objects.get(pk=comment.pk)


def test_create_comment_by_reader(news_detail_url, news, reader_client,
                                  reader):
    comments_before = set(Comment.objects.all())
    assertRedirects(
        reader_client.post(news_detail_url, data=NEW_TEXT_FOR_COMMENTS),
        f'{news_detail_url}#comments'
    )
    comments = set(Comment.objects.all()) - comments_before
    assert len(comments) == 1
    comment = comments.pop()
    assert comment.text == NEW_TEXT_FOR_COMMENTS['text']
    assert comment.news == news
    assert comment.author == reader


def test_create_comment_by_anonymous(
        client, news_detail_url, to_news_detail_url_after_login
):
    assert Comment.objects.count() == 0
    assertRedirects(
        client.post(news_detail_url, data=NEW_TEXT_FOR_COMMENTS),
        to_news_detail_url_after_login
    )
    assert Comment.objects.count() == 0


@pytest.mark.parametrize(
    'word',
    BAD_WORDS,
)
def test_comment_form_refuse_bad_words(news_detail_url, reader_client, word):
    assert Comment.objects.count() == 0
    assertFormError(
        reader_client.post(news_detail_url, data=dict(text=word)),
        'form',
        'text', WARNING
    )
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(
        comment, news_detail_url, author_client, comment_edit_url
):
    assertRedirects(
        author_client.post(comment_edit_url, data=NEW_TEXT_FOR_COMMENTS),
        f'{news_detail_url}#comments'
    )
    edited_comment = Comment.objects.get(pk=comment.pk)
    assert edited_comment.text == NEW_TEXT_FOR_COMMENTS['text']
    assert edited_comment.author == comment.author
    assert edited_comment.news == comment.news


def test_delete_comment_by_reader(comment, reader_client, comment_delete_url):
    comments_before = len(Comment.objects.all())
    reader_client.post(comment_delete_url)
    assert len(Comment.objects.all()) == comments_before
    comment_after = Comment.objects.get(pk=comment.pk)
    assert comment_after.text == comment.text
    assert comment_after.news == comment.news
    assert comment_after.author == comment.author
