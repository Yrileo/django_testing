from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.forms import NoteForm
from .mixin import TestMixinAuthorNoteReader, CreatNoteConstantTestMixin

User = get_user_model()


class TestContextNote(CreatNoteConstantTestMixin, TestMixinAuthorNoteReader):

    def test_context_note(self):

        url = reverse('notes:list')
        response = self.author_client.get(url)
        object_list = response.context['object_list']

        self.assertTrue(self.note in object_list)

    def test_list_notes_user_doesnt_appear_notes_another(self):

        users = (
            (self.author_client, True),
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
