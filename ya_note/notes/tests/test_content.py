from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.forms import NoteForm
from .mixin import TestMixinAuthorNoteReader, CreatNoteConstantTestMixin

User = get_user_model()


class TestContextNote(CreatNoteConstantTestMixin,
                      TestMixinAuthorNoteReader):

    list_url = reverse('notes:list')

    def test_context_note(self):
        response = self.author_client.get(self.list_url)
        object_list = response.context['object_list']
        self.assertTrue(self.note in object_list)

    def test_list_notes_user_doesnt_appear_notes_another(self):
        users = (
            (self.reader_client, False),
        )
        for client, value in users:
            with self.subTest(client=client):
                response = client.get(reverse('notes:list'))
                object_list = response.context['object_list']
                self.assertTrue(
                    (self.note in object_list) is value)

    def test_user_has_form(self):
        for url, kwargs in (
                ('notes:add', None),
                ('notes:edit', {'slug': self.note.slug})
        ):
            with self.subTest(url=url):
                url = reverse(url, kwargs=kwargs)
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
