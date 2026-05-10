# hellbox-metadata

A [hellbox](https://github.com/hellboxpy/hellbox) plugin for updating font metadata using [fonttools](https://github.com/fonttools/fonttools).

## Usage

```python
from hellbox import Hellbox
from hellbox.jobs.metadata import SetNames

with Hellbox("build") as task:
    task.read("build/*.ttf") >> SetNames(
        copyright="© 2024 My Foundry",
        version="Version 1.000",
        vendor_url="https://myfoundry.com",
        license_url="https://myfoundry.com/license",
    ) >> task.write("release")
```

`SetNames` updates all existing platform records for each field and adds a Windows Unicode record if none is present.

### Supported fields

| Keyword           | nameID | Description            |
| ----------------- | ------ | ---------------------- |
| `copyright`       | 0      | Copyright notice       |
| `family`          | 1      | Family name            |
| `subfamily`       | 2      | Subfamily name         |
| `unique_id`       | 3      | Unique font identifier |
| `full_name`       | 4      | Full font name         |
| `version`         | 5      | Version string         |
| `postscript_name` | 6      | PostScript name        |
| `trademark`       | 7      | Trademark              |
| `manufacturer`    | 8      | Manufacturer name      |
| `designer`        | 9      | Designer               |
| `description`     | 10     | Description            |
| `vendor_url`      | 11     | Vendor URL             |
| `designer_url`    | 12     | Designer URL           |
| `license`         | 13     | License description    |
| `license_url`     | 14     | License info URL       |

## Installation

```sh
hell add hellbox-metadata
```

## Development

```sh
uv sync
uv run pytest
```
