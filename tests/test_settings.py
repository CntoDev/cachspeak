import pytest

from cachspeak import settings


def test_unloaded_configurator():
    """Assert CachspeakConfigParser raises when used without having loaded a file."""
    config_parser = settings.CachspeakConfigParser()
    with pytest.raises(RuntimeError):
        config_parser.get('dummy_section', 'dummy_value')


@pytest.fixture(scope="module")
def config_file(tmpdir_factory):
    """Fixture that generates a usable configuration file."""
    tmpfile = tmpdir_factory.mktemp('data').join('config.ini')
    tmpfile.write(
        "[TestSection]\n"
        "key = value\n"
    )
    return tmpfile.strpath


def test_configurator_loading(config_file):
    """Assert CachspeakConfigParser successfully loads a configuration file."""
    config_parser = settings.CachspeakConfigParser()
    config_parser.read(config_file)


def test_configurator_fetching(config_file):
    """Assert CachspeakConfigParser successfully fetches a given setting."""
    config_parser = settings.CachspeakConfigParser()
    config_parser.read(config_file)
    assert config_parser.get('TestSection', 'key') == "value"
