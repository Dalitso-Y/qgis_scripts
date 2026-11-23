# Script authoring and QA guidelines

## Naming and layout

- Use `snake_case.py` with descriptive task names, e.g. `calculate_slope_statistics.py`.
- Keep **one primary workflow per script**. Extract reusable logic only when it improves maintenance.
- Organize by GIS task (terrain, raster, vector, etc.), not by the QGIS release.
- Include a module docstring with execution mode, inputs, outputs, dependencies, versions tested and limitations.
- Prefer parameters over fixed paths and fixed CRSs.

## Minimum script header

```python
"""Short purpose.

Execution: QGIS Python Console | Processing Toolbox | Standalone PyQGIS
Inputs: ...
Outputs: ...
Tested: QGIS x.y, Python x.y, operating system, date (or 'not tested')
Dependencies: ...
CRS / units: ...
Side effects: ...
Limitations: ...
"""
```

## Geospatial correctness

1. Validate feature geometry types and required fields before processing.
2. Require an explicit CRS or transform inputs deliberately. Never assume longitude/latitude coordinates have metric units.
3. State whether distance/area calculations are planar, ellipsoidal, or geodesic.
4. Distinguish raster pixel resolution, nodata, vertical units and horizontal units.
5. State the expected elevation datum if terrain accuracy depends on it.
6. Avoid unexpected edits; use a new output layer by default.
7. For large datasets, consider streaming, temporary layers, spatial indexing and cancellation.
8. Document any proprietary processing provider and its installation requirement.

## Testing checklist

- [ ] Empty layer / no selection
- [ ] Invalid geometries and missing attributes
- [ ] Different CRS and measurement units
- [ ] Nodata / null values
- [ ] Unexpected file paths, permissions and existing destinations
- [ ] Large inputs and cancellation (where relevant)
- [ ] QGIS versions actually claimed as compatible
- [ ] Expected output schema, feature count and/or test statistics
- [ ] No unrequested edits to input files

## Version compatibility

QGIS 3 and 4 can use different Qt/Python binding arrangements; do not promise universal compatibility without testing. Prefer documented QGIS APIs and avoid direct `PyQt5`/`PyQt6` imports where `qgis.PyQt` supplies the needed compatibility layer. Record tested versions in `docs/COMPATIBILITY.md`.

## Documentation example

```markdown
### `scripts/terrain/example.py`
- **Purpose:** Generate elevation statistics for a study area.
- **Execution:** Processing Toolbox.
- **Inputs:** DEM raster, study-area polygon.
- **Outputs:** Table with mean/min/max elevation.
- **CRS / units:** Projected CRS, vertical units in metres (verify before use).
- **Tested:** Not yet tested.
- **Risks:** Results depend on nodata and raster coverage.
```
