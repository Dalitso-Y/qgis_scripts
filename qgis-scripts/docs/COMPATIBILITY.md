# Compatibility matrix

Static Python checks in CI cannot verify availability of QGIS classes, processing providers, Qt compatibility or numerical correctness.

| QGIS family | Python/Qt environment | Repository status | Notes |
| --- | --- | --- | --- |
| QGIS 3.x | Depends on exact QGIS release | Not validated | Check the target release and library support individually |
| QGIS 4.x | Depends on exact QGIS release | Not validated | Review Qt6/SIP/API changes and test directly |

## Record tests at script level

Use an entry like:

```text
Script: scripts/utilities/list_loaded_layers.py
QGIS: [exact release]
Python: [exact release]
OS: [exact release]
Test date: YYYY-MM-DD
Input data: [sanitized public test fixture]
Outcome: pass/fail + notes
```

## Portability principles

- Prefer `qgis.core`, `qgis.gui` and `qgis.PyQt` from the installed QGIS environment.
- Distinguish syntax-only CI checks from QGIS runtime integration tests.
- Record GDAL/PROJ dependencies for algorithms sensitive to raster data and CRS transforms.
- Avoid labeling scripts as QGIS 3/4 compatible until they have passed the same representative tests on both.
