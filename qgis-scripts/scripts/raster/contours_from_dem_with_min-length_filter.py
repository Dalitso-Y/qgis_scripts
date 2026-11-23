#================================================================
# Developed by: Dalitso Yambani
# Linkedin profile: www.linkedin.com/in/dalitso-yambani-710868a8
# Email: dalitsoy@mirandgroup.co.zm
#================================================================

# -*- coding: utf-8 -*-
"""
QGIS 3.40.14 (PyQGIS) — Contours-from-DEM with length filtering + optional smoothing .

Runs in:
- QGIS Python Console (paste & run), or
- QGIS Script Editor (as a plain Python script)

Core Processing algorithms used:
- gdal:contour
- native:multiparttosingleparts
- native:simplifygeometries (Douglas–Peucker)
- native:smoothgeometry (Chaikin-like smoothing)
"""
#edit file_path to actual path of script file
#execution script: exec(open(r"file_path\contours_from_dem_with_min-length_filter.py", encoding="utf-8").read())

# ============================================================
# USER PARAMETERS (Edit here)
# ============================================================

dem_path = r""  # input DEM (GeoTIFF, etc.)

output_contours_path = r""  # GeoPackage or .shp

contour_interval = 10     # e.g. 1.0, 5.0
base_contour = 0.0          # "OFFSET" in GDAL contour
attribute_name = "ELEV"     # elevation field name in output

min_length = 20.0           # float or None. If set, removes shorter contours
length_unit_mode = "METERS" # "LAYER_UNITS" or "METERS"

smooth_iterations = 4       # int; 0 disables smoothing step entirely
smooth_offset = 0.5        # Chaikin "strength" (0..0.5 typical). For DouglasPeucker: tolerance fallback.
smooth_method = "Chaikin"   # "Chaikin" or "DouglasPeucker"

simplify_tolerance = None   # float or None. Optional DP simplification (layer units). Applied BEFORE Chaikin smoothing.

add_to_project = True       # add final output to the QGIS project

# ============================================================
# ADVANCED / INTERNAL DEFAULTS (edit only if you know why)
# ============================================================

_dem_band = 1               # DEM band for contouring
_smooth_max_angle = 180.0   # native:smoothgeometry; 180 means "smooth all nodes"
_output_gpkg_layer_name = "contours"  # layer name inside GeoPackage

# ============================================================
# IMPLEMENTATION
# ============================================================

import os
import pathlib
import processing

from qgis.PyQt.QtCore import QVariant
from qgis.core import (
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsFeature,
    QgsDistanceArea,
    QgsVectorFileWriter,
    QgsWkbTypes,
    QgsProcessingFeedback,
)

def _raise(msg: str):
    raise RuntimeError(msg)

def _as_vector_layer(obj, name="tmp") -> QgsVectorLayer:
    """
    processing.run() may return:
      - a path/URI string, or
      - (rarely) a QgsVectorLayer
    Normalize to QgsVectorLayer.
    """
    if isinstance(obj, QgsVectorLayer):
        return obj
    if obj is None:
        _raise("Processing returned None for a vector output.")
    vl = QgsVectorLayer(str(obj), name, "ogr")
    if not vl.isValid():
        _raise(f"Failed to load vector layer from: {obj}")
    return vl

def _check_paths():
    if not dem_path or not os.path.exists(dem_path):
        _raise(f"DEM path does not exist: {dem_path}")

    out_dir = os.path.dirname(output_contours_path)
    if out_dir and not os.path.exists(out_dir):
        _raise(f"Output directory does not exist: {out_dir}")

    ext = pathlib.Path(output_contours_path).suffix.lower()
    if ext not in (".gpkg", ".shp"):
        _raise("output_contours_path must end with .gpkg or .shp")

def _delete_existing_shapefile(path_shp: str):
    # Safest: let QGIS remove all sidecars
    if os.path.exists(path_shp):
        QgsVectorFileWriter.deleteShapeFile(path_shp)

def _run_alg(alg_id: str, params: dict, feedback: QgsProcessingFeedback):
    try:
        return processing.run(alg_id, params, feedback=feedback)
    except Exception as e:
        _raise(f"Processing failed for '{alg_id}': {e}")

def _apply_simplify_dp(input_vl: QgsVectorLayer, tolerance: float, feedback: QgsProcessingFeedback) -> QgsVectorLayer:
    if tolerance is None or tolerance <= 0:
        return input_vl

    res = _run_alg(
        "native:simplifygeometries",
        {
            "INPUT": input_vl,
            "METHOD": 0,            # 0 — Distance (Douglas-Peucker)
            "TOLERANCE": float(tolerance),
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
        feedback,
    )
    return _as_vector_layer(res["OUTPUT"], "simplified")

def _apply_smooth_chaikin(input_vl: QgsVectorLayer, iterations: int, offset: float, feedback: QgsProcessingFeedback) -> QgsVectorLayer:
    if iterations is None or iterations <= 0:
        return input_vl

    # Clamp offset to sane range used by QGIS smoothing docs/examples
    off = max(0.0, min(float(offset), 0.5))

    res = _run_alg(
        "native:smoothgeometry",
        {
            "INPUT": input_vl,
            "ITERATIONS": int(iterations),
            "OFFSET": off,
            "MAX_ANGLE": float(_smooth_max_angle),
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
        feedback,
    )
    return _as_vector_layer(res["OUTPUT"], "smoothed")

def _filter_by_length(input_vl: QgsVectorLayer, min_len: float, unit_mode: str) -> (QgsVectorLayer, int):
    """
    Returns (filtered_layer, removed_count).
    - LAYER_UNITS: uses geometry.length() in layer CRS units.
    - METERS: uses QgsDistanceArea in ellipsoidal mode to return meters regardless of CRS.
    """
    if min_len is None:
        return input_vl, 0

    unit_mode = (unit_mode or "").strip().upper()
    if unit_mode not in ("LAYER_UNITS", "METERS"):
        _raise("length_unit_mode must be 'LAYER_UNITS' or 'METERS'")

    # Create an in-memory layer with same schema/CRS
    wkb = input_vl.wkbType()
    crs = input_vl.crs()

    geom_name = QgsWkbTypes.displayString(wkb)
    mem_uri = f"{geom_name}?crs={crs.authid()}"
    out_vl = QgsVectorLayer(mem_uri, "contours_filtered", "memory")
    if not out_vl.isValid():
        # Fallback to generic linestring if provider rejects displayString in some edge cases
        out_vl = QgsVectorLayer(f"LineString?crs={crs.authid()}", "contours_filtered", "memory")
        if not out_vl.isValid():
            _raise("Failed to create memory layer for length filtering.")

    dp = out_vl.dataProvider()
    dp.addAttributes(input_vl.fields())
    out_vl.updateFields()
    out_vl.setCrs(crs)

    removed = 0

    dist = None
    if unit_mode == "METERS":
        dist = QgsDistanceArea()
        dist.setSourceCrs(crs, QgsProject.instance().transformContext())
        ellps = QgsProject.instance().ellipsoid() or "WGS84"
        dist.setEllipsoid("WGS84")

    features_to_add = []
    for f in input_vl.getFeatures():
        geom = f.geometry()
        if geom is None or geom.isEmpty():
            removed += 1
            continue

        if unit_mode == "LAYER_UNITS":
            L = geom.length()
        else:
            # meters (ellipsoidal)
            L = dist.measureLength(geom)

        if L < float(min_len):
            removed += 1
            continue

        nf = QgsFeature(out_vl.fields())
        nf.setGeometry(geom)
        nf.setAttributes(f.attributes())
        features_to_add.append(nf)

    dp.addFeatures(features_to_add)
    out_vl.updateExtents()
    return out_vl, removed

def _save_final(layer: QgsVectorLayer) -> (str, str):
    """
    Saves final layer to output_contours_path.
    Returns (written_filename, written_layername_for_gpkg_or_empty).
    """
    ext = pathlib.Path(output_contours_path).suffix.lower()
    if ext == ".shp":
        _delete_existing_shapefile(output_contours_path)
        driver = "ESRI Shapefile"
        layer_name = ""
    else:
        driver = "GPKG"
        layer_name = _output_gpkg_layer_name

    opts = QgsVectorFileWriter.SaveVectorOptions()
    opts.driverName = driver
    opts.fileEncoding = "UTF-8"

    if driver == "GPKG":
        opts.layerName = layer_name
        # If file exists, overwrite just the layer; if not, create file
        if os.path.exists(output_contours_path):
            opts.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
        else:
            opts.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile
    else:
        opts.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile

    err_code, new_filename, new_layer, err_msg = QgsVectorFileWriter.writeAsVectorFormatV3(
        layer,
        output_contours_path,
        QgsProject.instance().transformContext(),
        opts,
    )

    if err_code != QgsVectorFileWriter.NoError:
        _raise(f"Failed to write output. WriterError={int(err_code)}; message={err_msg}")

    return (new_filename or output_contours_path, new_layer or layer_name)

def main():
    _check_paths()
    feedback = QgsProcessingFeedback()

    # Validate DEM load (explicitly requested)
    dem_rl = QgsRasterLayer(dem_path, "DEM", "gdal")
    if not dem_rl.isValid():
        _raise(f"Failed to load DEM raster: {dem_path}")

    # 1) Generate contours (temporary output for deterministic post-processing)
    contour_params = {
        "INPUT": dem_path,
        "BAND": int(_dem_band),
        "INTERVAL": float(contour_interval),
        "FIELD_NAME": str(attribute_name) if attribute_name else None,
        "OFFSET": float(base_contour),
        "CREATE_3D": False,
        "IGNORE_NODATA": False,
        "NODATA": None,
        "EXTRA": "",
        "OUTPUT": "TEMPORARY_OUTPUT",
    }
    res_contour = _run_alg("gdal:contour", contour_params, feedback)
    contours_vl = _as_vector_layer(res_contour["OUTPUT"], "contours_raw")

    # Optional: enforce single-part (helps ensure LineString features)
    res_single = _run_alg(
        "native:multiparttosingleparts",
        {"INPUT": contours_vl, "OUTPUT": "TEMPORARY_OUTPUT"},
        feedback,
    )
    contours_vl = _as_vector_layer(res_single["OUTPUT"], "contours_single")

    count_generated = contours_vl.featureCount()

    # 2) Post-process (simplify/smooth)
    smoothing_used = "None"
    # If DouglasPeucker is the chosen smoothing method and smoothing is enabled,
    # DP tolerance comes from simplify_tolerance (if set) otherwise smooth_offset.
    if smooth_iterations and int(smooth_iterations) > 0:
        if (smooth_method or "").strip() == "DouglasPeucker":
            tol = simplify_tolerance if simplify_tolerance is not None else smooth_offset
            contours_vl = _apply_simplify_dp(contours_vl, tol, feedback)
            smoothing_used = f"DouglasPeucker (tolerance={tol} layer units; iterations ignored)"
        elif (smooth_method or "").strip() == "Chaikin":
            # Optional pre-simplification BEFORE Chaikin smoothing:
            # This reduces high-frequency wiggles before smoothing and helps avoid vertex explosion.
            if simplify_tolerance is not None:
                contours_vl = _apply_simplify_dp(contours_vl, simplify_tolerance, feedback)

            contours_vl = _apply_smooth_chaikin(contours_vl, int(smooth_iterations), float(smooth_offset), feedback)
            smoothing_used = f"Chaikin via native:smoothgeometry (iterations={smooth_iterations}, offset={smooth_offset}, max_angle={_smooth_max_angle})"
        else:
            _raise("smooth_method must be 'Chaikin' or 'DouglasPeucker'")
    else:
        # If smoothing is disabled but simplify_tolerance is set, apply it (still useful for de-zigzag).
        if simplify_tolerance is not None:
            contours_vl = _apply_simplify_dp(contours_vl, simplify_tolerance, feedback)
            smoothing_used = f"Smoothing disabled; simplification applied (DouglasPeucker tolerance={simplify_tolerance} layer units)"
        else:
            smoothing_used = "Smoothing disabled"

    # 3) Length filter (optional)
    contours_final_vl, removed_by_length = _filter_by_length(contours_vl, min_length, length_unit_mode)

    # 4) Save final
    written_filename, written_layer = _save_final(contours_final_vl)

    # 5) Add to project (optional)
    if add_to_project:
        if pathlib.Path(written_filename).suffix.lower() == ".gpkg":
            uri = f"{written_filename}|layername={written_layer}"
            out_layer = QgsVectorLayer(uri, "Contours", "ogr")
        else:
            out_layer = QgsVectorLayer(written_filename, "Contours", "ogr")

        if out_layer.isValid():
            QgsProject.instance().addMapLayer(out_layer)
        else:
            print(f"Warning: output written but could not be loaded into project: {written_filename}")

    # Summary
    final_count = contours_final_vl.featureCount()
    print("============================================================")
    print("Contour generation + post-processing complete")
    print(f"Contours generated (after singlepart): {count_generated}")
    print(f"Contours removed by length filter:     {removed_by_length}")
    print(f"Contours in final output:             {final_count}")
    print(f"Smoothing / simplification:           {smoothing_used}")
    if min_length is not None:
        print(f"Min length threshold:                 {min_length} ({length_unit_mode})")
    print(f"Written to:                           {written_filename}" + (f" (layer={written_layer})" if written_layer else ""))
    print("============================================================")

# Run now
main()
