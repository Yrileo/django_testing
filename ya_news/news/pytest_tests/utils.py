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
