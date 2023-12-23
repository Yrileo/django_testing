from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client
from pytils.translit import slugify
from notes.forms import WARNING
from notes.models import Note
from .mixin import (
    TestCheck, CreatNoteConstantTestMixin, CreateTestNoteMixin,
    DeleteEditTestNoteMixin, UpdateNoteConstantTestMixin,
    UniqueSlugCreationMixin
)

User = get_user_model()


class TestNoteCreation(TestCheck,
                       CreatNoteConstantTestMixin,
                       CreateTestNoteMixin,
                       UniqueSlugCreationMixin):

    def test_unique_slug_field(self):
        self.create_duplicate_note()
        response = self.author_client.post(
            self.add_note_url, data=self.form_data
        )
        self.assertFormError(response,
                             form='form', field='slug',
                             errors=f'{self.NOTE_SLUG}{WARNING}')


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
        self.assertTrue(Note.objects.filter(
            text=self.form_data['text'],
            slug=self.form_data['slug'],
            author=self.author
        ).exists())

    def test_anonymous_cant_create_note(self):
        note_count_current = Note.objects.count()
        self.client.post(self.add_note_url, data=self.form_data)
        note_count = Note.objects.count()
        self.assertEqual(note_count_current, note_count)

    def test_user_can_create_note(self):
        note_count_before = Note.objects.count()
        response = self.author_client.post(
            self.add_note_url, data=self.form_data
        )
        self.assertRedirects(response, self.success_url)
        note_count_after = Note.objects.count()
        self.assertEqual(note_count_before + 1, note_count_after)
        self.assertTrue(
            Note.objects.filter(title=self.form_data['title']).exists()
        )
        new_note = Note.objects.get(title=self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])

    def the_field_is_empty_slug_will_generated(self):
        expected_slug = slugify(self.form_data['title'])
        response = self.author_client.post(
            self.add_note_url, data=self.form_data
        )
        self.assertRedirects(response, self.success_url)
        note = Note.objects.get(title=self.form_data['title'])
        self.assertEqual(expected_slug, note.slug)


class TestNoteEditDelete(CreatNoteConstantTestMixin,
                         TestCheck,
                         UpdateNoteConstantTestMixin,
                         DeleteEditTestNoteMixin):

    def test_author_can_edit_note(self):
        response = self.author_client.post(self.url_edit, data=self.form_data)
        self.assertRedirects(response, self.success_url)
        self.note.refresh_from_db()
        note = Note.objects.get(title=self.form_data['title'])
        self.check(
            note,
            self.form_data['title'],
            self.form_data['text'],
            self.form_data['slug']
        )

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(self.url_edit, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.check(self.note, self.NOTE_TITLE, self.NOTE_TEXT, self.NOTE_SLUG)
        self.assertEqual(self.note.author, self.author)

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
        self.assertEqual(original_note.author, self.author)
