from http import HTTPStatus

from pytils.translit import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note
from notes.forms import WARNING

User = get_user_model()


class TestNoteCreation(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.slug = 'slug'
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.author_to = User.objects.create(username='Тоже автор')
        cls.author_to_client = Client()
        cls.author_to_client.force_login(cls.author_to)
        cls.form_data = {'title': 'Form title',
                         'text': 'Form text',
                         'slug': cls.slug}
        cls.note = Note.objects.create(
            title='Form title',
            text='Form text',
            slug=cls.slug,
            author=cls.author,
        )
        cls.form_data_no_slug = {
            'title': 'Form title',
            'text': 'Form text',
        }
        cls.url_add = reverse('notes:add')
        cls.url_edit = reverse('notes:edit', args=(cls.slug,))
        cls.url_delete = reverse('notes:delete', args=(cls.slug,))
        cls.url_success = reverse('notes:success')
        cls.login_url = reverse('users:login')

    def test_unique_slug_field(self):
        count_old = Note.objects.count()
        response = self.author_client.post(self.url_add, data=self.form_data)
        count_new = Note.objects.count()
        self.assertEqual(count_old, count_new)
        warning = self.form_data['slug'] + WARNING
        self.assertFormError(
            response, form='form', field='slug', errors=warning
        )

    def test_user_can_create_note(self):
        note = Note.objects.all()
        Note.objects.all().delete()
        response = self.author_client.post(self.url_add, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(note.last().title, self.form_data['title'])
        self.assertEqual(note.last().text, self.form_data['text'])
        self.assertEqual(note.last().slug, self.form_data['slug'])
        self.assertEqual(note.last().author, self.author)

    def test_anonymous_cant_create_note(self):
        count_old = Note.objects.count()
        response = self.client.post(self.url_add, data=self.form_data)
        count_new = Note.objects.count()
        self.assertEqual(count_old, count_new)
        expected_url = f'{self.login_url}?next={self.url_add}'
        self.assertRedirects(response, expected_url)

    def test_field_is_empty_slug_will_generated(self):
        Note.objects.all().delete()
        self.client.force_login(self.author)
        self.form_data.pop('slug')
        response = self.client.post(self.url_add, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), 1)
        expected_slug = slugify(self.form_data['title'])
        new_note = Note.objects.last()
        self.assertEqual(new_note.title, self.form_data_no_slug['title'])
        self.assertEqual(new_note.text, self.form_data_no_slug['text'])
        self.assertEqual(new_note.slug, expected_slug)
        self.assertEqual(new_note.author, self.author)


class TestNoteEditDelete(TestCase):
    NOTE_TITLE = 'Текст заголовка'
    NEW_NOTE_TITLE = 'Новый текст заголовка'
    NOTE_TEXT = 'Текст заметки'
    NEW_NOTE_TEXT = 'Новый текст заметка'
    NEW_NOTE_SLUG = 'new-slug'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title=cls.NOTE_TITLE,
            text=cls.NOTE_TEXT,
            slug='note-slug',
            author=cls.author,
        )
        cls.url_edit = reverse('notes:edit', args=[cls.note.slug])
        cls.url_delete = reverse('notes:delete', args=[cls.note.slug])
        cls.form_data = {
            'title': cls.NEW_NOTE_TITLE,
            'text': cls.NEW_NOTE_TEXT,
            'slug': cls.NEW_NOTE_SLUG
        }

    def test_author_can_edit_note(self):
        count_old = Note.objects.count()
        self.author_client.post(self.url_edit, self.form_data)
        count_new = Note.objects.count()
        self.assertEqual(count_old, count_new)
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.note.author)

    def test_user_cant_edit_note_of_another_user(self):
        count_old = Note.objects.count()
        response = self.reader_client.post(self.url_edit, self.form_data)
        count_new = Note.objects.count()
        self.assertEqual(count_old, count_new)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        new_note = Note.objects.last()
        self.assertEqual(self.note.title, new_note.title)
        self.assertEqual(self.note.text, new_note.text)
        self.assertEqual(self.note.slug, new_note.slug)
        self.assertEqual(self.note.author, new_note.author)

    def test_author_can_delete_note(self):
        count_old = Note.objects.count()
        response = self.author_client.post(self.url_delete)
        count_new = Note.objects.count()
        self.assertEqual(count_new, count_old - 1)
        self.assertRedirects(response, reverse('notes:success'))

    def test_user_cant_delete_note_of_another_user(self):
        count_old = Note.objects.count()
        response = self.reader_client.post(self.url_delete)
        count_new = Note.objects.count()
        self.assertEqual(count_new, count_old)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
