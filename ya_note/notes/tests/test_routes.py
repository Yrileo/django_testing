from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse

from .mixin import CreatNoteConstantTestMixin, TestNoteMixin

User = get_user_model()


class TestRoutes(CreatNoteConstantTestMixin, TestNoteMixin):
    def setUp(self):
        super().setUp()
        self.URLS = {
            'list': reverse('notes:list'),
            'success': reverse('notes:success'),
            'add': reverse('notes:add'),
            'detail': reverse('notes:detail', kwargs={'slug': self.note.slug}),
            'edit': reverse('notes:edit', kwargs={'slug': self.note.slug}),
            'delete': reverse('notes:delete', kwargs={'slug': self.note.slug}),
            'home': reverse('notes:home'),
            'login': reverse('users:login'),
            'logout': reverse('users:logout'),
            'signup': reverse('users:signup'),
        }

    def test_authornote(self):
        for name, url in self.URLS.items():
            with self.subTest(name=name):
                response = self.author_client.get(url, follow=True)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability(self):
        for name, url in self.URLS.items():
            with self.subTest(name=name):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, HTTPStatus.OK)
