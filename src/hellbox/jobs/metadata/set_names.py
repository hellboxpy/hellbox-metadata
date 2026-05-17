from fontTools import ttLib

from hellbox import Chute, Hellbox

# Maps friendly keyword argument names to OpenType nameID integers.
NAME_IDS = {
    "copyright": 0,
    "family": 1,
    "subfamily": 2,
    "unique_id": 3,
    "full_name": 4,
    "version": 5,
    "postscript_name": 6,
    "trademark": 7,
    "manufacturer": 8,
    "designer": 9,
    "description": 10,
    "vendor_url": 11,
    "designer_url": 12,
    "license": 13,
    "license_url": 14,
}


def _update_name(name_table, name_id, value):
    existing = [r for r in name_table.names if r.nameID == name_id]
    if existing:
        for record in existing:
            name_table.setName(
                value, name_id, record.platformID, record.platEncID, record.langID
            )
    else:
        name_table.setName(value, name_id, 3, 1, 0x0409)


class SetNames(Chute):
    """SetNames updates name table records in a font file.

    Pass name fields as keyword arguments using friendly names:

        SetNames(copyright="© 2024 Foundry", version="Version 1.000")

    Supported fields: copyright, family, subfamily, unique_id, full_name,
    version, postscript_name, trademark, manufacturer, designer, description,
    vendor_url, designer_url, license, license_url.
    """

    def __init__(self, **names):
        unknown = set(names) - set(NAME_IDS)
        if unknown:
            raise ValueError(f"Unknown name fields: {', '.join(sorted(unknown))}")
        self.names = {NAME_IDS[k]: v for k, v in names.items()}

    def process(self, file):
        Hellbox.info(f"Setting names: {file.name}")
        copy = file.copy()
        font = ttLib.TTFont(copy.content_path)
        for name_id, value in self.names.items():
            _update_name(font["name"], name_id, value)
        font.save(copy.content_path)
        return copy
