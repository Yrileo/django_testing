from http import HTTPStatus

from django.contrib.auth import get_user_model
from pytils.translit import slugify
from notes.forms import WARNING
from notes.models import Note
from .mixin import (
    TestCheck, CreatNoteConstantTestMixin, CreateTestNoteMixin,
    DeleteEditTestNoteMixin, UpdateNoteConstantTestMixin
)

User = get_user_model()


class TestNoteCreation(TestCheck,
                       CreatNoteConstantTestMixin,
                       CreateTestNoteMixin):

    def test_user_can_create_note(self):
        response = self.author_client.post(
            self.add_note_url, data=self.form_data
        )
        self.assertRedirects(response, self.success_url)
        note = Note.objects.last()
        self.check(note, self.NOTE_TITLE, self.NOTE_TEXT, self.NOTE_SLUG)

    def test_anonymous_cant_create_note(self):
        note_count_current = Note.objects.count()
        self.client.post(self.add_note_url, data=self.form_data)
        note_count = Note.objects.count()
        self.assertEqual(note_count_current, note_count)

    def test_unique_slug_field(self):
        Note.objects.create(
            title=self.NOTE_TITLE,
            text=self.NOTE_TEXT,
            slug=self.NOTE_SLUG,
            author=self.author,
        )
        response = self.author_client.post(
            self.add_note_url, data=self.form_data
        )
        self.assertFormError(response,
                             form='form', field='slug',
                             errors=f'{self.NOTE_SLUG}{WARNING}')

    def the_field_is_empty_slug_will_generated(self):
        self.form_data.pop('slug')
        expected_slug = slugify(self.form_data['title'])
        self.assertRedirects(
            self.author_client.post(self.url, data=self.form_data),
            self.success_url
        )
        self.author_client.post(self.url, data=self.form_data)
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
            self.NEW_NOTE_TITLE,
            self.NEW_NOTE_TEXT,
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

    def test_user_cant_delete_note_of_another_user(self):
        note_count_current = Note.objects.count()
        response = self.reader_client.delete(self.url_delete)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_count = Note.objects.count()
        self.assertEqual(note_count_current, note_count)
