import os
import stat

import pytest

from cachspeak import persistence


def test_persistence_bad_perms(tmpdir_factory):
    """Assert presistent_storage throws an error on insecure database file"""
    tmpfile_path = str(tmpdir_factory.mktemp('data').join('database.pickle3'))
    with open(tmpfile_path, 'x') as _:
        pass
    os.chmod(tmpfile_path, (stat.S_IRUSR | stat.S_IWUSR |
                            stat.S_IRGRP | stat.S_IWGRP |
                            stat.S_IROTH | stat.S_IWOTH))
    with pytest.raises(RuntimeError):
        with persistence.persistent_storage(tmpfile_path) as _:
            pass # pragma: no cover


def test_persistence(tmpdir_factory):
    """Assert persistent data can be stored and retrieved."""
    tmpfile_path = str(tmpdir_factory.mktemp('data').join('database.pickle3'))

    persisted_value = "test_value"
    with persistence.persistent_storage(tmpfile_path) as storage:
        storage["test_key"] = persisted_value
    with persistence.persistent_storage(tmpfile_path) as storage:
        assert storage["test_key"] == persisted_value
