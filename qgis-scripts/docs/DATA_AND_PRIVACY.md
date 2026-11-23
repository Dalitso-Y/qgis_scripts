# Data, privacy, and licensing

A public script repository must not contain private client datasets or redistributed GIS data without permission.

## Keep out of Git

- Client survey data, cadastral records, coordinates of sensitive infrastructure, personal information and confidential work products.
- Credentials, API keys, service-account files, tokens and private endpoint URLs.
- Unlicensed basemaps, imagery, elevation models, and third-party styles/assets.
- Large processing outputs or project-specific scratch datasets (use `data/`, `outputs/`, `temp/` locally, ignored by Git).

## Appropriate sample data

Use a **small, synthetic or openly licensed** dataset under `examples/` and include its source, license and CRS. Avoid embedding actual client coordinates even if names are removed. If large public datasets are required, provide download links and reproduction instructions instead of committing them.

## Source and third-party code

Before copying an existing script into this repository, verify its owner, redistribution rights, license compatibility and attribution requirements. The repository's proposed MIT license does not automatically relicense third-party source code or GIS datasets.

## Check before publishing

- Review Git history for accidental secrets; deleting the file from the latest commit is not sufficient to remove it from history.
- Inspect project files and data source URIs for embedded credentials and private paths.
- Verify that documentation screenshots, logos and samples can be published.
