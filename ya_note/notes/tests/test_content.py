from notes.forms import NoteForm
from notes.models import Note

from .configurations import TestBaseParameters, Urls


class TestContent(TestBaseParameters):
    def test_note_displays_for_author(self):
        self.assertEqual(
            len(
                self.author_client.get(Urls.NOTES_LIST).context['object_list']
            ),
            Note.objects.count()
        )
        self.assertIn(
            self.note,
            self.author_client.get(Urls.NOTES_LIST).context['object_list']
        )
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(
            (note.title, note.text, note.slug, note.author),
            (self.note.title, self.note.text, self.note.slug, self.note.author)
        )

    def test_note_displays_for_reader(self):
        self.assertNotIn(
            self.note,
            self.reader_client.get(Urls.NOTES_LIST).context['object_list']
        )

    def test_form_at_add_and_edit_urls(self):
        testing_urls = (
            Urls.NOTE_EDIT, Urls.NOTE_ADD
        )
        for url in testing_urls:
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.author_client.get(url).context.get('form'),
                    NoteForm
                )
