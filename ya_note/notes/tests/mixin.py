from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class CreatNoteConstantTestMixin:

    NOTE_TITLE = 'Тестовая заметка.'
    NOTE_TEXT = 'Текст заметки'
    NOTE_SLUG = 'slug-test-1'


class UpdateNoteConstantTestMixin:

    NEW_NOTE_TITLE = 'New Тестовая заметка.'
    NEW_NOTE_TEXT = 'New Текст заметки'
    NEW_NOTE_SLUG = 'new-slug-test-1'


class TestMixinAuthor:

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Фамилия Имя')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)


class CreateTestNoteMixin(TestMixinAuthor, TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.add_note_url = reverse('notes:add')
        cls.success_url = reverse('notes:success')
        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_TEXT,
            'slug': cls.NOTE_SLUG
        }


class TestNoteMixin(TestMixinAuthor, TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.note = Note.objects.create(
            title=cls.NOTE_TITLE,
            text=cls.NOTE_TEXT,
            slug=cls.NOTE_SLUG,
            author=cls.author
        )


class TestMixinAuthorNoteReader(TestNoteMixin):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)


class DeleteEditTestNoteMixin(TestMixinAuthorNoteReader):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.success_url = reverse('notes:success')
        cls.url_edit = reverse('notes:edit', kwargs={'slug': cls.note.slug})
        cls.url_delete = reverse('notes:delete', kwargs={
            'slug': cls.note.slug})
        cls.form_data = {
            'title': cls.NEW_NOTE_TITLE,
            'text': cls.NEW_NOTE_TEXT,
            'slug': cls.NEW_NOTE_SLUG
        }


class TestCheck(TestCase):
    def check(self, notes, title, text, slug):
        data = (notes.title, notes.text, notes.slug)
        const_data = (title, text, slug)
        for db_value, value in zip(
            data, const_data
        ):
            with self.subTest(db_value=db_value, value=value):
                self.assertEqual(
                    db_value,
                    value
                )


class UniqueSlugCreationMixin(TestMixinAuthor):

    @classmethod
    def create_duplicate_note(cls):
        return Note.objects.create(
            title=cls.NOTE_TITLE,
            text=cls.NOTE_TEXT,
            slug=cls.NOTE_SLUG,
            author=cls.author
        )


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
