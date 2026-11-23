# Tests

`test_repository_structure.py` runs with ordinary Python and checks starter-file consistency. The GitHub workflow also statically compiles scripts and runs Ruff. **None of these tests executes the PyQGIS runtime.**

Once actual workflows are added, create integration tests that use the QGIS Python environment and record the tested QGIS/GDAL/PROJ versions. Avoid running destructive tests on production files.
