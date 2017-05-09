import os
import pytest
import pytest_mock

import cachspeak
from test_cachet import cachet_response
from test_utils import load_from_json
from test_teamspeak import TS3ConnectionMock


@pytest.fixture(scope='module')
def saved_status_no_updates():
    return load_from_json('saved_status_no_updates.json')


@pytest.fixture(scope='module')
def saved_status_multi_updates():
    return load_from_json('saved_status_multi_updates.json')


def create_test_persist_file(data, tmpdir_factory):
    file_path = str(tmpdir_factory.mktemp('data').join('persist_file.db'))
    with cachspeak.persistence.persistent_storage(file_path) as storage:
        storage['last_status'] = data

    return file_path


def test_main_no_updates(mocker, tmpdir_factory, saved_status_no_updates, cachet_response):
    """Assert that no messages are sent if no components were updated"""
    mock_cachet = mocker.patch('cachetclient.cachet.Components.get')
    mock_ts3 = mocker.patch('ts3.query.TS3Connection', new=TS3ConnectionMock)
    mock_ts3.sendtextmessage = mocker.Mock()

    mock_cachet.return_value = cachet_response
    persist_file = create_test_persist_file(data=saved_status_no_updates, tmpdir_factory=tmpdir_factory)

    config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures', 'cachspeak.ini')

    cachspeak.main(config_path=config_path, persist_path=persist_file)

    assert mock_ts3.sendtextmessage.call_count == 0


def test_main_with_updates(mocker, tmpdir_factory, saved_status_multi_updates, cachet_response):
    """Assert that messages are sent for proper updated components"""
    mock_cachet = mocker.patch('cachetclient.cachet.Components.get')
    mock_ts3 = mocker.patch('ts3.query.TS3Connection', new=TS3ConnectionMock)
    mock_ts3.sendtextmessage = mocker.Mock()

    mock_cachet.return_value = cachet_response
    persist_file = create_test_persist_file(data=saved_status_multi_updates, tmpdir_factory=tmpdir_factory)

    config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures', 'cachspeak.ini')

    cachspeak.main(config_path=config_path, persist_path=persist_file, debug=True)

    assert mock_ts3.sendtextmessage.call_count == 3
