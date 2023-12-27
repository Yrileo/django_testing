from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class Text:
    NOTE_TITLE = 'Название'
    NOTE_TEXT = 'Название Текста'
    NOTE_SLUG = 'slug'
    NEW_PREFIX = 'EDITED_'
    NEW_NOTE_TITLE = NEW_PREFIX + NOTE_TITLE
    NEW_NOTE_TEXT = NEW_PREFIX + NOTE_TEXT
    NEW_NOTE_SLUG = NEW_PREFIX + NOTE_SLUG


class Urls:
    HOME = reverse('notes:home')
    NOTE_ADD = reverse('notes:add')
    NOTES_LIST = reverse('notes:list')
    USER_LOGIN = reverse('users:login')
    USER_LOGOUT = reverse('users:logout')
    USER_SIGNUP = reverse('users:signup')
    NOTES_SUCCESS = reverse('notes:success')
    NOTE_EDIT = reverse('notes:edit', args=(Text.NOTE_SLUG,))
    NOTE_DELETE = reverse('notes:delete', args=(Text.NOTE_SLUG,))
    NOTE_DETAIL = reverse('notes:detail', args=(Text.NOTE_SLUG,))
    REDIRECT_TO_NOTE_ADD = f'{USER_LOGIN}?next={NOTE_ADD}'
    REDIRECT_TO_NOTE_EDIT = f'{USER_LOGIN}?next={NOTE_EDIT}'
    REDIRECT_TO_NOTE_DETAIL = f'{USER_LOGIN}?next={NOTE_DETAIL}'
    REDIRECT_TO_NOTE_DELETE = f'{USER_LOGIN}?next={NOTE_DELETE}'


class TestBaseParameters(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Reader')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.anonymous_client = Client()
        cls.note = Note.objects.create(
            author=cls.author,
            title=Text.NOTE_TITLE,
            text=Text.NOTE_TEXT,
            slug=Text.NOTE_SLUG,
        )
        cls.new_note_data = dict(
            title=Text.NEW_NOTE_TITLE,
            text=Text.NEW_NOTE_TEXT,
            slug=Text.NEW_NOTE_SLUG,
        )
        cls.edit_note_data = dict(
            title=Text.NEW_NOTE_TITLE,
            text=Text.NEW_NOTE_TEXT,
            slug=Text.NOTE_SLUG,
        )
        cls.no_slug_note_data = dict(
            title=Text.NEW_NOTE_TITLE,
            text=Text.NEW_NOTE_TEXT,
        )
