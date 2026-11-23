"""TODO: Briefly state what this script does.

Execution: QGIS Python Console.
Inputs: TODO
Outputs: TODO
Tested: Not tested.
Dependencies: QGIS Desktop / PyQGIS.
CRS / units: TODO
Side effects: TODO
Limitations: TODO

Copy this file into the appropriate GIS task category, rename it, and update this header.
"""

from qgis.core import QgsProject


def main():
    project = QgsProject.instance()
    print(f"Project: {project.fileName() or '[unsaved project]'}")
    # TODO: Implement the workflow here. Do not modify source data by default.


if __name__ == "__main__":
    main()
