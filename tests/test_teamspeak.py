import pytest
import pytest_mock

import ts3

from cachspeak import teamspeak


class TS3ConnectionMock(ts3.query.TS3Connection):
    """Mocks original class to prevent host/credentials check"""

    def __init__(self, host=None, port=10011):
        pass

    def close(self):
        pass

    def use(self, *, sid=None, port=None, virtual=False):
        pass

    def login(self, *, client_login_name, client_login_password):
        pass

    def clientupdate(self, **client_properties):
        pass


@pytest.fixture()
def messages():
    return ['First message', 'Second message', 'Third message', 'Fourth message']


@pytest.fixture()
def credentials():
    return dict(host='test_host', username='test_username', password='test_password')


def test_teamspeak_send_with_messages(messages, credentials, mocker):
    mock_connection = mocker.patch('ts3.query.TS3Connection', new=TS3ConnectionMock)
    mock_connection.sendtextmessage = mocker.Mock()

    teamspeak.send_global_messages(messages=messages, **credentials)

    assert mock_connection.sendtextmessage.call_count == len(messages)


def test_teamspeak_send_no_messages(credentials, mocker):
    mock_connection = mocker.patch('ts3.query.TS3Connection', new=TS3ConnectionMock)
    mock_connection.sendtextmessage = mocker.Mock()

    teamspeak.send_global_messages(messages=[], **credentials)

    assert mock_connection.sendtextmessage.call_count == 0
