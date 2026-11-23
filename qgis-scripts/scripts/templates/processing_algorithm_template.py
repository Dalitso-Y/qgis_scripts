"""Template: a minimal QGIS Processing algorithm with a parameter and output.

Execution: QGIS Processing Toolbox script editor.
Inputs: Text parameter.
Outputs: Text result (no new GIS data).
Tested: Not yet validated in a QGIS installation.
Dependencies: QGIS Processing framework.
CRS / units: Not applicable.
Side effects: None.
Limitations: This only demonstrates the algorithm structure.

Copy and rename this file before implementing a real geospatial operation.
"""

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingOutputString,
    QgsProcessingParameterString,
)


class ProcessingAlgorithmTemplate(QgsProcessingAlgorithm):
    INPUT_TEXT = "INPUT_TEXT"
    OUTPUT_TEXT = "OUTPUT_TEXT"

    def name(self):
        return "processing_algorithm_template"

    def displayName(self):
        return "Processing algorithm template (example)"

    def group(self):
        return "Script templates"

    def groupId(self):
        return "script_templates"

    def shortHelpString(self):
        return "Returns the entered text to demonstrate QGIS Processing parameters."

    def createInstance(self):
        return ProcessingAlgorithmTemplate()

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterString(self.INPUT_TEXT, "Text to return")
        )
        self.addOutput(QgsProcessingOutputString(self.OUTPUT_TEXT, "Returned text"))

    def processAlgorithm(self, parameters, context, feedback):
        text = self.parameterAsString(parameters, self.INPUT_TEXT, context)
        if feedback.isCanceled():
            return {self.OUTPUT_TEXT: ""}
        feedback.pushInfo("Template executed; no GIS data was changed.")
        return {self.OUTPUT_TEXT: text}
