import pytest


class Urls:
    NEWS_HOME = pytest.lazy_fixture('news_home_url')
    NEWS_DETAIL = pytest.lazy_fixture('news_detail_url')
    NEWS_DELETE = pytest.lazy_fixture('comment_delete_url')
    NEWS_EDIT = pytest.lazy_fixture('comment_edit_url')
    LOGIN = pytest.lazy_fixture('login_url')
    LOGOUT = pytest.lazy_fixture('logout_url')
    SIGNUP = pytest.lazy_fixture('signup_url')
    REDIRECT_EDIT = pytest.lazy_fixture('to_news_edit_url_after_login')
    REDIRECT_DELETE = pytest.lazy_fixture('to_news_delete_url_after_login')


class UsrClient:
    ANONYMOUS = pytest.lazy_fixture('client')
    READER = pytest.lazy_fixture('reader_client')
    AUTHOR = pytest.lazy_fixture('author_client')
