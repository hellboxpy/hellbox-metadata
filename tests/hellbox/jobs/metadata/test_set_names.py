import pytest
from unittest.mock import MagicMock, patch

from hellbox.jobs.metadata import SetNames
from hellbox.jobs.metadata.set_names import _update_name


class TestUpdateName:
    def test_updates_existing_records(self):
        record = MagicMock()
        record.nameID = 0
        record.platformID = 3
        record.platEncID = 1
        record.langID = 0x0409
        name_table = MagicMock()
        name_table.names = [record]

        _update_name(name_table, 0, "© 2024")

        name_table.setName.assert_called_once_with("© 2024", 0, 3, 1, 0x0409)

    def test_adds_windows_record_when_missing(self):
        name_table = MagicMock()
        name_table.names = []

        _update_name(name_table, 0, "© 2024")

        name_table.setName.assert_called_once_with("© 2024", 0, 3, 1, 0x0409)

    def test_updates_all_platforms(self):
        mac_record = MagicMock()
        mac_record.nameID = 0
        mac_record.platformID = 1
        mac_record.platEncID = 0
        mac_record.langID = 0

        win_record = MagicMock()
        win_record.nameID = 0
        win_record.platformID = 3
        win_record.platEncID = 1
        win_record.langID = 0x0409

        name_table = MagicMock()
        name_table.names = [mac_record, win_record]

        _update_name(name_table, 0, "© 2024")

        assert name_table.setName.call_count == 2


class TestSetNames:
    def test_init(self):
        assert SetNames(copyright="© 2024")

    def test_init_stores_name_ids(self):
        s = SetNames(copyright="© 2024", version="Version 1.000")
        assert s.names == {0: "© 2024", 5: "Version 1.000"}

    def test_init_rejects_unknown_fields(self):
        with pytest.raises(ValueError, match="Unknown name fields: bogus"):
            SetNames(bogus="value")

    def test_process(self):
        file = MagicMock()
        copy = MagicMock()
        file.copy.return_value = copy

        with (
            patch("hellbox.jobs.metadata.set_names.ttLib") as mock_ttlib,
            patch("hellbox.jobs.metadata.set_names._update_name") as mock_update,
        ):
            mock_font = MagicMock()
            mock_ttlib.TTFont.return_value = mock_font

            result = SetNames(copyright="© 2024", version="Version 1.000").process(file)

        assert mock_update.call_count == 2
        mock_font.save.assert_called_once_with(copy.content_path)
        assert result is copy
