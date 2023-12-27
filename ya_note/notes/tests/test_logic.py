from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note
from notes.forms import WARNING

from .configurations import TestBaseParameters, Urls


class TestClass(TestBaseParameters):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.notes_before = set(Note.objects.all())

    def test_created_note_with_and_without_slug(self):
        creation_cases = (
            (self.new_note_data, self.new_note_data['slug']),
            (self.no_slug_note_data, slugify(self.no_slug_note_data['title'])),
        )
        for data, expected_slug in creation_cases:
            with self.subTest(data=data, expected_slug=expected_slug):
                notes_at_start = set(Note.objects.all())
                self.assertRedirects(
                    self.author_client.post(Urls.NOTE_ADD, data=data),
                    Urls.NOTES_SUCCESS
                )
                note_objects = (set(Note.objects.all()) - notes_at_start)
                self.assertEqual(len(note_objects), 1)
                note = note_objects.pop()
                self.assertEqual(
                    (note.slug, note.title, note.text, note.author),
                    (expected_slug, data['title'], data['text'], self.author)
                )

    def test_anonymous_user_cant_create_note(self):
        self.assertRedirects(
            self.anonymous_client.post(Urls.NOTE_ADD,
                                       data=self.new_note_data),
            Urls.REDIRECT_TO_NOTE_ADD
        )
        self.assertEqual(
            self.notes_before, set(Note.objects.all())
        )

    def test_cant_use_slug_again(self):
        self.new_note_data['slug'] = self.note.slug
        self.assertFormError(
            self.author_client.post(Urls.NOTE_ADD, data=self.new_note_data),
            form='form',
            field='slug',
            errors=self.new_note_data['slug'] + WARNING
        )
        self.assertEqual(
            self.notes_before, set(Note.objects.all())
        )

    def test_author_can_edit(self):
        self.assertEqual(
            self.reader_client.post(
                Urls.NOTE_EDIT, data=self.edit_note_data
            ).status_code,
            HTTPStatus.NOT_FOUND
        )
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(
            (note.title, note.text, note.author, note.slug),
            (self.note.title, self.note.text, self.note.author, self.note.slug)
        )

    def test_author_can_delete_note(self):
        self.author_client.delete(Urls.NOTE_DELETE)
        self.assertEqual(Note.objects.count(), len(self.notes_before) - 1)
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_reader_cant_delete_note(self):
        self.reader_client.delete(Urls.NOTE_DELETE)
        self.assertTrue(Note.objects.filter(pk=self.note.pk).exists())
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(
            (note.title, note.text, note.author, note.slug),
            (self.note.title, self.note.text, self.note.author, self.note.slug)
        )
