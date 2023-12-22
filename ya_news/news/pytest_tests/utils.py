import pytest
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture

ADMIN = lazy_fixture('admin_client')
AUTHOR = lazy_fixture('author_client')
CLIENT = lazy_fixture('client')
PK = lazy_fixture('pk_news')
FORM_DATA = {
    'text': 'Новый комментарий'
}

URL = {
    'home': 'news:home',
    'detail': 'news:detail',
    'edit': 'news:edit',
    'delete': 'news:delete',
    'login': 'users:login',
    'logout': 'users:logout',
    'signup': 'users:signup',
}


# так ?
@pytest.fixture
def url_home():
    return reverse(URL['home'])


@pytest.fixture
def url_detail(pk):
    return reverse(URL['detail'], args=[pk])


@pytest.fixture
def url_edit(pk):
    return reverse(URL['edit'], args=[pk])


@pytest.fixture
def url_delete(pk):
    return reverse(URL['delete'], args=[pk])


@pytest.fixture
def url_login():
    return reverse(URL['login'])


@pytest.fixture
def url_logout():
    return reverse(URL['logout'])


@pytest.fixture
def url_signup():
    return reverse(URL['signup'])
