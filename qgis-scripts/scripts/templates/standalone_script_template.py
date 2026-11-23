"""Template for a standalone PyQGIS process.

Execution: QGIS-configured Python environment (outside QGIS Desktop).
Inputs: QGIS_PREFIX_PATH environment variable.
Outputs: QGIS runtime version text; no saved files.
Tested: Not yet validated in a QGIS installation.
Dependencies: QGIS installation and configured runtime libraries.
CRS / units: Not applicable.
Side effects: Initializes then shuts down the QGIS application.
Limitations: Requires OS-specific QGIS Python/library environment configuration.
"""

import os

from qgis.core import Qgis, QgsApplication


def main():
    prefix = os.environ.get("QGIS_PREFIX_PATH")
    if not prefix:
        raise RuntimeError("Set QGIS_PREFIX_PATH to the installed QGIS prefix")

    QgsApplication.setPrefixPath(prefix, True)
    app = QgsApplication([], False)
    app.initQgis()
    try:
        print(f"QGIS runtime version: {Qgis.QGIS_VERSION}")
        # TODO: Implement a read-only workflow, then add explicit output arguments.
    finally:
        app.exitQgis()


if __name__ == "__main__":
    main()
