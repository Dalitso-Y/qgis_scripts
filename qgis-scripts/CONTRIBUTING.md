# Contributing

Contributions that improve QGIS workflows, documentation, test coverage, or portability are welcome.

## Before opening a pull request

1. Search existing issues to avoid duplication.
2. For substantial changes, describe the use case in an issue first.
3. Use a focused branch, such as `feat/terrain-slope-report` or `fix/geometry-validation`.
4. Add scripts under the **task category**, not under a QGIS version folder. Create a category only when the existing categories do not fit.
5. Start from the closest template in `scripts/templates/`.
6. Include a complete module-level header and update `docs/SCRIPT_CATALOG.md`.
7. Add a test or explain how the workflow was manually verified. Document the exact QGIS, Python, OS and relevant provider versions tested.
8. Run the static checks shown in `README.md` and check file changes for confidential data.

## Technical rules

- Prefer clear, reusable functions and descriptive `snake_case` filenames.
- Avoid machine-specific paths, credentials, client identifiers, and hard-coded CRS choices.
- Declare whether areas/distances use projected, geodesic, or ellipsoidal measurements.
- Validate input layers, geometry types, field names, CRS and output destinations.
- Avoid silently overwriting source files. If a script is destructive, warn the user and require explicit opt-in.
- Processing tools should report progress and cancellation via `feedback` where possible.
- Log actionable errors; do not silently discard exceptions.
- Prefer QGIS APIs and dependency versions appropriate to the stated QGIS release.
- Do not add proprietary imagery, licensed basemaps, private client datasets, or credentials.

## Suggested pull request content

Explain the problem, approach, test environment, input/output data, before/after behavior, and compatibility changes. Link the relevant issue where applicable.

## Code of conduct

By participating, you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
