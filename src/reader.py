"""
Module for parsing input data
"""

from typing import Union
import pandas as pd
from src.utils import parse_input


class MetabolonCDT:
    """
    A class for reading and working with with Metabolon Client Data Table files.

    Attributes:
    - data_key_and_explanation: DataFrame containing data key and explanation.
    - sample_metadata: DataFrame containing sample metadata (required).
    - chemical_annotation: DataFrame containing chemical annotation (required).
    - peak_area_data: DataFrame containing peak area data and a column with the sample names. (required)
    - batch_normalized_data: DataFrame containing batch-normalized data and a column with the sample names. (optional)
    - batch_normalized_imputed_data: DataFrame containing batch-norm imputed data and a column with the sample names. (optional)
    - log_transformed_data: DataFrame containing log-transformed data and a column with the sample names.(optional)
    """

    def __init__(self) -> None:
        """
        Initialize the class.
        """
        self.data_key_and_explanation = None
        self.sample_metadata = None
        self.chemical_annotation = None
        self.peak_area_data = None
        self.batch_normalized_data = None
        self.batch_normalized_imputed_data = None
        self.log_transformed_data = None
        self.additional_data = {}

    def import_excel(self, file_path: str) -> None:
        """
        Read the Metabolon Client Data Table Excel file and assign its sheets to class attributes.

        Args:
            file_path (str): The file path to the Metabolon Excel file.

        Raises:
            ValueError: If any required sheet ('Sample Meta Data', 'Chemical Annotation',
            'Peak Area Data') is missing from the Excel file.
        """
        # Read Excel file
        sheets = pd.read_excel(file_path, sheet_name=None)

        # Check if required sheets are missing
        missing_sheets = [
            sheet_name
            for sheet_name in [
                "Sample Meta Data",
                "Chemical Annotation",
                "Peak Area Data",
            ]
            if sheet_name not in sheets
        ]
        if missing_sheets:
            raise ValueError(
                "The following required sheets are missing: {}".format(missing_sheets)
            )

        # Assign sheets to attributes
        self.data_key_and_explanation = sheets.pop("Data Key & Explanation", None)
        """DataFrame containing data key and explanation, if present in the Excel file."""
        self.sample_metadata = sheets.pop("Sample Meta Data")
        """DataFrame containing sample metadata."""
        self.chemical_annotation = sheets.pop("Chemical Annotation")
        """DataFrame containing chemical annotation."""
        self.peak_area_data = sheets.pop("Peak Area Data")
        """DataFrame containing peak area data and a column with the sample names."""
        self.batch_normalized_data = sheets.pop("Batch-normalized Data", None)
        """DataFrame containing batch-normalized data and a column with the sample names,
        if present in the Excel file."""
        self.batch_normalized_imputed_data = sheets.pop("Batch-norm Imputed Data", None)
        """DataFrame containing batch-norm imputed data and a column with the sample names,
        if present in the Excel file."""
        self.log_transformed_data = sheets.pop("Log Transformed Data", None)
        """DataFrame containing log-transformed data and a column with the sample names,
        if present in the Excel file."""
        self.additional_data = sheets
        """Dictionary of additional sheets found in the Excel file, keyed by sheet name."""

    def import_tables(
        self,
        sample_metadata: Union[pd.DataFrame, str],
        chemical_annotation: Union[pd.DataFrame, str],
        peak_area_data: Union[pd.DataFrame, str] = None,
        batch_normalized_data: Union[pd.DataFrame, str] = None,
        batch_normalized_imputed_data: Union[pd.DataFrame, str] = None,
        log_transformed_data: Union[pd.DataFrame, str] = None,
        generic_data: Union[pd.DataFrame, str] = None,
    ) -> None:
        """
        Read flat tables for sample metadata, chemical annotation, and metabolite data.

        Args:
            sample_metadata: DataFrame or path of file containing sample metadata (required).
            chemical_annotation: DataFrame or path of file containing chemical annotation (required).
            peak_area_data: DataFrame or path of file containing metabolite data (required).

        Raises:
            ValueError: If any required sheet ('Sample Meta Data', 'Chemical Annotation',
             'Peak Area Data') is missing from the Excel file.
        """
        # TODO: handling of other metabolite data such as batch normalized, log transformed etc
        # instead of generic metabolite_data
        # Read sample metadata
        self.sample_metadata = parse_input(sample_metadata)
        # Read chemical annotation
        self.chemical_annotation = parse_input(chemical_annotation)
        # Read peak area data
        try:
            self.peak_area_data = parse_input(peak_area_data)
        except TypeError:
            self.peak_area_data = None
        # Read batch normalized data
        try:
            self.batch_normalized_data = parse_input(batch_normalized_data)
        except TypeError:
            self.batch_normalized_data = None
        # Read batch normalized imputed data
        try:
            self.batch_normalized_imputed_data = parse_input(
                batch_normalized_imputed_data
            )
        except TypeError:
            self.batch_normalized_imputed_data = None
        # Read log transformed data
        try:
            self.log_transformed_data = parse_input(log_transformed_data)
        except TypeError:
            self.log_transformed_data = None
        # Read generic data
        try:
            self.generic_data = parse_input(generic_data)
        except TypeError:
            self.generic_data = None
