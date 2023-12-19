from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client
from pytils.translit import slugify

from notes.models import Note
from .mixin import (
    TestCheck, CreatNoteConstantTestMixin, CreateTestNoteMixin,
    DeleteEditTestNoteMixin, UpdateNoteConstantTestMixin
)

# какая-то фигня получилось, не нравится мне как код выглядит
User = get_user_model()


class TestNoteCreation(TestCheck,
                       CreatNoteConstantTestMixin,
                       CreateTestNoteMixin):

    def setUp(self):
        super().setUp()
        self.author_client = Client()
        self.author_client.force_login(self.author)

    def test_user_can_create_note(self):
        note_count_before = Note.objects.count()
        response = self.author_client.post(
            self.add_note_url, data=self.form_data
        )
        self.assertRedirects(response, self.success_url)
        note_count_after = Note.objects.count()
        self.assertEqual(note_count_before + 1, note_count_after)
        note = Note.objects.last()
        self.check(note, self.NOTE_TITLE, self.NOTE_TEXT, self.NOTE_SLUG)

    def test_anonymous_cant_create_note(self):
        note_count_current = Note.objects.count()
        self.client.post(self.add_note_url, data=self.form_data)
        note_count = Note.objects.count()
        self.assertEqual(note_count_current, note_count)

    def the_field_is_empty_slug_will_generated(self):
        expected_slug = slugify(self.form_data['title'])
        self.form_data.pop('slug')
        response = self.author_client.post(
            self.add_note_url, data=self.form_data
        )
        self.assertRedirects(response, self.success_url)
        note = Note.objects.last()
        self.assertEqual(expected_slug, note.slug)


class TestNoteEditDelete(CreatNoteConstantTestMixin,
                         TestCheck,
                         UpdateNoteConstantTestMixin,
                         DeleteEditTestNoteMixin):

    def test_author_can_edit_note(self):
        response = self.author_client.post(self.url_edit, data=self.form_data)
        self.assertRedirects(response, self.success_url)
        self.note.refresh_from_db()
        note = Note.objects.last()
        self.check(
            note,
            self.form_data['title'],
            self.form_data['text'],
            self.NEW_NOTE_SLUG
        )

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(self.url_edit, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.check(self.note, self.NOTE_TITLE, self.NOTE_TEXT, self.NOTE_SLUG)

    def test_author_can_delete_note(self):
        note_count_current = Note.objects.count()
        response = self.author_client.delete(self.url_delete)
        self.assertRedirects(response, self.success_url)
        note_count = Note.objects.count()
        self.assertEqual(note_count_current - 1, note_count)
        self.assertIsNone(Note.objects.filter(id=self.note.id).first())

    def test_user_cant_delete_note_of_another_user(self):
        note_count_current = Note.objects.count()
        response = self.reader_client.delete(self.url_delete)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_count = Note.objects.count()
        self.assertEqual(note_count_current, note_count)
        original_note = Note.objects.filter(id=self.note.id).first()
        self.assertIsNotNone(original_note)
        self.assertEqual(original_note.title, self.NOTE_TITLE)
        self.assertEqual(original_note.text, self.NOTE_TEXT)
        self.assertEqual(original_note.slug, self.NOTE_SLUG)
