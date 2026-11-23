# QGIS Scripts

A curated collection of Python and PyQGIS scripts for GIS data management, vector and raster processing, terrain analysis, remote sensing, cartography, engineering surveying, and workflow automation in QGIS.

## Contents

| Category | Typical tasks | Directory |
| --- | --- | --- |
| Vector processing | Geometry checks, attributes, overlays, conversions | [`scripts/vector/`](scripts/vector/) |
| Raster processing | Raster preparation, statistics, resampling | [`scripts/raster/`](scripts/raster/) |
| Terrain analysis | DEMs, contours, slope, elevation workflows | [`scripts/terrain/`](scripts/terrain/) |
| Remote sensing | Imagery processing and classification workflows | [`scripts/remote_sensing/`](scripts/remote_sensing/) |
| Surveying | Coordinates, survey QA, engineering survey workflows | [`scripts/surveying/`](scripts/surveying/) |
| Cartography | Map layouts, labeling and export automation | [`scripts/cartography/`](scripts/cartography/) |
| Automation | Batch jobs, project operations, repeatable pipelines | [`scripts/automation/`](scripts/automation/) |
| Utilities | Diagnostics and general-purpose helpers | [`scripts/utilities/`](scripts/utilities/) |
| Templates | Starting points for new scripts | [`scripts/templates/`](scripts/templates/) |

See the [script catalog](docs/SCRIPT_CATALOG.md) for descriptions and per-script status.

## Quick start

1. **Install QGIS** from the [official QGIS website](https://qgis.org/).
2. Download or clone the repository.
3. Choose a script in the [catalog](docs/SCRIPT_CATALOG.md). Read its header and any associated documentation.
4. Check QGIS compatibility and required input data. Work with copies of important files.
5. Run it using the method stated in the script: Python Console, Processing Toolbox, or a configured standalone PyQGIS environment.

### Example: QGIS Python Console

Open **Plugins → Python Console** in QGIS. Update this path to your cloned repository location:

```python
import runpy
runpy.run_path(r"C:\path\to\qgis-scripts\scripts\utilities\list_loaded_layers.py", run_name="__main__")
```

The starter utility reports the loaded layers, their types, and CRS identifiers; it does **not** modify any layer.

### Processing algorithm scripts

Open **Processing Toolbox → Scripts → Create new script** and use the QGIS script editor, or install the `.py` file in QGIS's active Processing scripts folder. Use QGIS's Processing settings to locate that folder rather than assuming a fixed operating-system path. Processing algorithms must use a valid `QgsProcessingAlgorithm` implementation (or supported decorator approach).

### Standalone PyQGIS scripts

Standalone scripts require a **QGIS-aware Python environment** and proper initialization of `QgsApplication`. Do not assume that `pip install qgis` into a normal Python environment will reproduce an installed desktop QGIS. See [Getting Started](docs/GETTING_STARTED.md).

## Documentation

- [Getting started and execution methods](docs/GETTING_STARTED.md)
- [Script catalog](docs/SCRIPT_CATALOG.md)
- [Script authoring and QA guidelines](docs/SCRIPT_GUIDELINES.md)
- [Compatibility matrix](docs/COMPATIBILITY.md)
- [Data, licensing, and privacy practices](docs/DATA_AND_PRIVACY.md)
- [Repository structure](docs/REPOSITORY_TREE.md)
- [Publishing to GitHub](docs/PUBLISHING.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)

## Script documentation standard

Each added script should specify its **purpose, execution method, QGIS/Python versions tested, inputs, outputs, dependencies, CRS/units assumptions, usage, and known limitations**. For workflows with measurable outputs, include a small, openly licensed test dataset and expected results when feasible. Use the [catalog](docs/SCRIPT_CATALOG.md) to register scripts.

## Quality checks

From the repository root, use regular Python for static checks (QGIS installation is **not** necessary for these checks):

```bash
python -m compileall -q scripts
python -m unittest discover -s tests -v
```

An optional lint check uses `ruff` (install using `python -m pip install -r requirements-dev.txt`):

```bash
ruff check scripts tests
```

GitHub Actions executes the same **static** checks. Passing CI **does not establish runtime compatibility with QGIS**; run geospatial functionality tests in the documented QGIS environment.

## Contributing and licensing

Contributions and bug reports are welcome; please read [CONTRIBUTING.md](CONTRIBUTING.md). The repository template contains an **MIT License with a copyright**. Before publication, confirm the ownership of code and replace `[Dalitso Yambani]` in [`LICENSE`](LICENSE). Only contribute code and datasets you have permission to redistribute. QGIS and third-party packages remain subject to their own licenses.

## References

- [PyQGIS Developer Cookbook](https://docs.qgis.org/3.44/en/docs/pyqgis_developer_cookbook/)
- [QGIS Processing script documentation](https://docs.qgis.org/3.44/en/docs/user_manual/processing/scripts.html)
- [QGIS Project](https://qgis.org/)
