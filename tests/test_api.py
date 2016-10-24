import json
import pytest

import airtable


@pytest.fixture
def api_key():
    return "FOO"


@pytest.fixture
def base_url():
    return "airtable.com/foo/bar"


@pytest.fixture
def airtable_request_monkeypatch():
    pass


@pytest.fixture
def config_file(tmpdir, api_key, base_url):
    config_file = tmpdir.join('config.yaml')
    with open(str(config_file), 'w') as fh:
        json.dump({'api_key': api_key, 'base_url': base_url}, fh)

    return str(config_file)


class TestBase:
    def test__init__(self, api_key, base_url):
        test_base = airtable.Base(api_key, base_url)
        assert test_base is not None
        assert isinstance(test_base, airtable.Base)

    def test__init__from_config_file(self,
                                     config_file):
        test_base = airtable.Base.from_config(config_file)
        assert test_base is not None
        assert isinstance(test_base, airtable.Base)

    def test__repr__(self, api_key, base_url):
        test_base = airtable.Base(api_key, base_url)
        assert test_base is not None
        assert isinstance(test_base, airtable.Base)

        assert isinstance(str(test_base), str)
        assert 'Base' in str(test_base)
        assert 'base_url' in str(test_base)

    def test_table(self, api_key, base_url):
        test_base = airtable.Base(api_key, base_url)
        table = test_base.table('foo')
        assert isinstance(table, airtable.Table)

        table = test_base['foo']
        assert isinstance(table, airtable.Table)


class TestTable:
    def test__get__(self, airtable_request_monkeypatch):
        pass

    def test__create(self, airtable_request_monkeypatch):
        """Test creating a record."""
        pass

    def test__update(self, airtable_request_monkeypatch):
        """Test updating a record."""
        pass

    def test__delete(self):
        """Test deleting a record."""
        pass

    def test__to_df(self):
        """Return the contents of a table as a pandas dataframe."""
        pass

    def test__update_from_df(self):
        """Update the contents of a table given a pandas dataframe
        which matches the structure of the table.
        """
        pass
