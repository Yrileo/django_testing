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
        client, value = self.reader_client, False
        response = client.get(self.list_url)
        object_list = response.context['object_list']
        self.assertEqual((self.note in object_list), value)

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
