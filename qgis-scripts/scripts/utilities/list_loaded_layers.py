"""Display layers loaded in the active QGIS project.

Execution: QGIS Python Console (use runpy.run_path).
Inputs: Currently open QGIS project.
Outputs: Human-readable lines in the Python Console; no saved files.
Tested: Not yet validated in a QGIS installation.
Dependencies: QGIS Python bindings provided by QGIS Desktop.
CRS / units: Reports each layer's CRS identifier; performs no measurement.
Side effects: None (read-only).
Limitations: Does not inspect nested layer tree visibility or remote-layer availability.
"""

from qgis.core import QgsProject


def main():
    """Print basic properties of all layers registered in the current project."""
    layers = QgsProject.instance().mapLayers().values()
    count = 0

    for layer in sorted(layers, key=lambda item: item.name().casefold()):
        count += 1
        name = layer.name()
        layer_type = layer.type().name if hasattr(layer.type(), "name") else str(layer.type())
        crs_id = layer.crs().authid() or "unknown / custom CRS"
        status = "valid" if layer.isValid() else "invalid"
        print(f"{count:>3}. {name} | type={layer_type} | CRS={crs_id} | {status}")

    print(f"Total registered layers: {count}")


if __name__ == "__main__":
    main()
