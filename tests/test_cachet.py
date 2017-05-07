import json
import pytest
import pytest_mock

from test_utils import load_from_json
from cachspeak import cachet


@pytest.fixture(scope='module')
def cachet_client():
    return cachet.CachetAPI(endpoint='test_endpoint')


@pytest.fixture(scope='module')
def cachet_response():
    return json.dumps(load_from_json('cachet_response.json'))


@pytest.fixture(scope='module')
def matching_list():
    return load_from_json('matching_components_list.json')

@pytest.fixture(scope='module')
def matching_cases():
    return load_from_json('matching_components_cases.json')


def test_normal_components_fetch(mocker, cachet_client, cachet_response):
    """Assert the number of components retrieved from Cachet response is valid"""
    mock_get = mocker.patch('cachetclient.cachet.Components.get')
    mock_get.return_value = cachet_response

    fetched_components = cachet_client.components

    decoded_response = json.loads(cachet_response)

    assert len(fetched_components) == len(tuple(decoded_response['data']))


def test_keep_component_fields(mocker, cachet_client, cachet_response):
    """Assert every component contains only data specified in cachet.COMPONENT_DATA"""
    mock_get = mocker.patch('cachetclient.cachet.Components.get')
    mock_get.return_value = cachet_response

    fetched_components = cachet_client.components

    for component in fetched_components:
        assert component.keys() == cachet.COMPONENT_DATA


def test_matching_component_no_match(cachet_client, matching_list, matching_cases):
    """Assert find_matching_component returns None if no component match"""
    match_result = cachet_client.find_matching_component(matching_cases['no_match_component'], matching_list)

    assert match_result is None


def test_matching_component_single_match(cachet_client, matching_list, matching_cases):
    """Assert find_matching_component returns a single element for single match"""
    match_result = cachet_client.find_matching_component(matching_cases['single_match_component'], matching_list)

    assert match_result is not None
    assert match_result == matching_cases['single_match_result']


def test_matching_component_multiple_match(cachet_client, matching_list, matching_cases):
    """Assert find_matching_component returns last updated component for multiple match"""
    match_result = cachet_client.find_matching_component(matching_cases['double_match_component'], matching_list)

    assert match_result is not None
    assert match_result == matching_cases['double_match_result']


def test_updated_components_none_saved(mocker, cachet_client, cachet_response):
    """Assert if no status is saved all components are considered updated"""
    mock_get = mocker.patch('cachetclient.cachet.Components.get')
    mock_get.return_value = cachet_response

    updated_components = list(cachet_client.updated_components([]))

    assert updated_components == list(cachet_client.components)


def test_updated_components_two_updated(mocker, cachet_client, cachet_response):
    """Assert the right components are considered updated"""
    mock_get = mocker.patch('cachetclient.cachet.Components.get')
    mock_get.return_value = cachet_response

    status = load_from_json('updated_components_two_updated.json')

    updated_components = list(cachet_client.updated_components(status))

    assert len(updated_components) == 2
    assert any(comp['id'] == 3 for comp in updated_components)
    assert any(comp['id'] == 6 for comp in updated_components)


def test_updated_components_none_updated(mocker, cachet_client, cachet_response):
    """Assert no components are considered updated if there are no actual changes"""
    mock_get = mocker.patch('cachetclient.cachet.Components.get')
    mock_get.return_value = cachet_response

    status = load_from_json('updated_components_none_updated.json')

    updated_components = list(cachet_client.updated_components(status))

    assert len(updated_components) == 0
