from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUp(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Новая заметка',
            text='Очень новая заметка',
            slug='note-slug',
            author=cls.author
        )
        cls.slug = [cls.note.slug]
        cls.url_home = reverse('notes:home')
        cls.url_list = reverse('notes:list')
        cls.url_detail = reverse('notes:detail', args=cls.slug)
        cls.url_edit = reverse('notes:edit', args=cls.slug)
        cls.url_delete = reverse('notes:delete', args=cls.slug)
        cls.url_success = reverse('notes:success')
        cls.login_url = reverse('users:login')
        cls.url_add = reverse('notes:add')
        cls.logout_url = reverse('users:logout')
        cls.signup_url = reverse('users:signup')
        cls.cortege_urls = (
            cls.url_home,
            cls.url_list,
            cls.url_detail,
            cls.url_edit,
            cls.url_delete,
            cls.url_success,
            cls.login_url,
            cls.url_add,
            cls.logout_url,
            cls.signup_url
        )
        cls.banned_urls_reader = (cls.url_detail,
                                  cls.url_edit,
                                  cls.url_delete)
        cls.banned_urls_client = (cls.url_add,
                                  cls.url_success,
                                  cls.url_delete,
                                  cls.url_edit,
                                  cls.url_detail,
                                  cls.url_list)

    def test_authornote(self):
        for url in self.cortege_urls:
            with self.subTest(url=url):
                res = self.author_client.get(url)
                self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_pages_availability(self):
        for url in self.cortege_urls:
            with self.subTest(url=url):
                response = self.reader_client.get(url)
                expected_status = (
                    HTTPStatus.OK if url not in self.banned_urls_reader
                    else HTTPStatus.NOT_FOUND
                )
                self.assertEqual(response.status_code, expected_status)

    def test_redirects(self):
        for url in self.cortege_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                expected_status = (
                    HTTPStatus.OK if url not in self.banned_urls_client
                    else HTTPStatus.FOUND
                )
                self.assertEqual(response.status_code, expected_status)
