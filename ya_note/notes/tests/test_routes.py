from http import HTTPStatus

from .configurations import TestBaseParameters, Urls


class TestRoutes(TestBaseParameters):
    def test_urls_status_cods(self):
        testing_urls = (
            (self.anonymous_client, Urls.HOME, HTTPStatus.OK),
            (self.anonymous_client, Urls.USER_LOGIN, HTTPStatus.OK),
            (self.anonymous_client, Urls.USER_LOGOUT, HTTPStatus.OK),
            (self.anonymous_client, Urls.USER_SIGNUP, HTTPStatus.OK),
            (self.reader_client, Urls.NOTE_ADD, HTTPStatus.OK),
            (self.reader_client, Urls.NOTES_LIST, HTTPStatus.OK),
            (self.reader_client, Urls.NOTES_SUCCESS, HTTPStatus.OK),
            (self.author_client, Urls.NOTE_EDIT, HTTPStatus.OK),
            (self.author_client, Urls.NOTE_DELETE, HTTPStatus.OK),
            (self.author_client, Urls.NOTE_DETAIL, HTTPStatus.OK),
            (self.reader_client, Urls.NOTE_EDIT, HTTPStatus.NOT_FOUND),
            (self.reader_client, Urls.NOTE_DELETE, HTTPStatus.NOT_FOUND),
            (self.reader_client, Urls.NOTE_DETAIL, HTTPStatus.NOT_FOUND),
        )
        for client, url, status in testing_urls:
            with self.subTest(clint=client, url=url, status=status):
                self.assertEqual(client.get(url).status_code, status)

    def test_urls_redirect(self):
        testing_urls = (
            (self.anonymous_client, Urls.NOTE_EDIT,
             Urls.REDIRECT_TO_NOTE_EDIT),
            (self.anonymous_client, Urls.NOTE_DETAIL,
             Urls.REDIRECT_TO_NOTE_DETAIL),
            (self.anonymous_client, Urls.NOTE_DELETE,
             Urls.REDIRECT_TO_NOTE_DELETE),
        )
        for client, urls, redirect_to in testing_urls:
            with self.subTest(
                client=client, urls=urls, redirect_to=redirect_to
            ):
                self.assertRedirects(
                    client.get(urls), redirect_to,
                )
