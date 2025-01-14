# -*- coding: utf-8 -*-
"""
This module contains tools and utilities for integrating the STARWARS model with ArcGIS Pro
and calculating volumetric water content (VWC) averages from multiple stations.
"""

# Standard Libraries
import os
import sys
import locale
import warnings
import time
import shutil
import string
import numpy as np
from datetime import datetime, timedelta

# Third-Party Libraries
import arcpy
from arcpy.sa import *
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
from matplotlib.offsetbox import AnchoredText
import pandas as pd
import psycopg2
from osgeo import gdal
from osgeo import ogr

# PCRaster Libraries
import pcraster as pcr
from pcraster import DynamicModel

# Suppress warnings from matplotlib
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

# Locale Settings
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Set matplotlib to use non-interactive backend
matplotlib.use('agg')

# Define Tools
class Toolbox(object):
    """
    The main toolbox containing tools for integrating the STARWARS model with ArcGIS Pro.

    Attributes:
        label (str): Display name of the toolbox.
        alias (str): Alias for the toolbox.
        tools (list): List of tools in the toolbox.
    """

    def __init__(self):
        self.label = "STARWARS Tools"
        self.alias = "starwars_tools"
        self.tools = [StarwarsModelTool, AveragingTool]


class StarwarsModelTool(object):
    """
    Tool for integrating and running the STARWARS model in ArcGIS Pro.

    Attributes:
        label (str): Display name of the tool.
        description (str): Description of the tool's functionality.
        canRunInBackground (bool): Specifies if the tool can run in the background.
    """

    def __init__(self):
        self.label = "STARWARS Model Tool"
        self.description = "Integrate and run the STARWARS hydrological model within ArcGIS Pro."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """
        Define tool parameters.

        Returns:
            list: List of `arcpy.Parameter` objects for the tool.
        """
        # Parameters to be defined as required
        return []

    def execute(self, parameters, messages):
        """
        Execute the STARWARS model with the provided parameters.

        Args:
            parameters (list): Tool parameters.
            messages (arcpy.Messages): ArcGIS messaging object.
        """
        pass


class AveragingTool(object):
    """
    Tool to calculate average Volumetric Water Content (VWC) from multiple stations.
    """

    def __init__(self):
        self.label = "VWC Averaging Tool"
        self.description = (
            "Process modeled Volumetric Water Content (VWC) data from multiple stations to "
            "calculate averages and generate summary plots."
        )
        self.canRunInBackground = False

    def getParameterInfo(self):
        """
        Define parameters required by the tool.

        Returns:
            list: List of `arcpy.Parameter` objects.
        """
        params = []

        # DEM input parameter
        dem_input = arcpy.Parameter(
            displayName="DEM Raster Input",
            name="dem_input",
            datatype="Raster Layer",
            parameterType="Required",
            direction="Input"
        )
        params.append(dem_input)

        # Dynamically define station and folder parameters up to 15 pairs
        max_stations = 15
        for i in range(1, max_stations + 1):
            if i > 2:  # Add checkbox for additional stations
                add_station = arcpy.Parameter(
                    displayName=f"Add Station {i}",
                    name=f"add_station_{i}",
                    datatype="Boolean",
                    parameterType="Optional",
                    direction="Input"
                )
                params.append(add_station)

            station = arcpy.Parameter(
                displayName=f"Station {i}",
                name=f"station_{i}",
                datatype="Feature Layer",
                parameterType="Optional" if i > 2 else "Required",
                direction="Input"
            )
            station.filter.list = ["Point", "Polygon"]
            params.append(station)

            folder = arcpy.Parameter(
                displayName=f"VWC Folder {i}",
                name=f"folder_{i}",
                datatype="DEFolder",
                parameterType="Optional" if i > 2 else "Required",
                direction="Input"
            )
            params.append(folder)

        # Output parameters
        output_avg_vwc = arcpy.Parameter(
            displayName="Output Average VWC Folder",
            name="output_avg_vwc",
            datatype="DEFolder",
            parameterType="Required",
            direction="Output"
        )
        params.append(output_avg_vwc)

        output_plot = arcpy.Parameter(
            displayName="Output Plot for Average VWC",
            name="output_plot",
            datatype="DEFile",
            parameterType="Required",
            direction="Output"
        )
        output_plot.filter.list = ["jpg"]
        params.append(output_plot)

        return params

    def updateParameters(self, parameters):
        """
        Dynamically enable/disable parameters based on user input.

        Args:
            parameters (list): List of `arcpy.Parameter` objects.
        """
        start_index = 3
        step = 3
        max_stations = 15

        for i in range(3, max_stations + 1):
            base_index = start_index + (i - 1) * step
            checkbox = parameters[base_index - 3]
            station = parameters[base_index - 2]
            folder = parameters[base_index - 1]

            if checkbox.value:
                station.enabled = True
                folder.enabled = True
            else:
                station.enabled = False
                station.value = None
                folder.enabled = False
                folder.value = None

        return parameters

    def execute(self, parameters, messages):
        """
        Process VWC data and calculate averages.

        Args:
            parameters (list): List of input parameters.
            messages (arcpy.Messages): ArcGIS messaging object.
        """
        # Implement the tool logic here
        pass