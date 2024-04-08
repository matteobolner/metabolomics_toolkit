import numpy as np
import pandas as pd
from src.utils import validate_dataframe

class MissingDataHandler:
    """
    Class for detecting and counting missing values in data,
    as well as removing columns/rows based on their missing data content.

    Attributes:
        threshold (float): Maximum ratio of missingness for dropping columns or rows.

    Methods:
        __init__(threshold=0.25): Initializes the MissingDataHandler with the specified threshold.
        detect_missing(data): Detects missing values in a collection.
        count_missing(data_frame, axis=0): Counts missing values in each row or column of a DataFrame.
        drop_columns_with_missing(data_frame): Removes columns with missing values above the threshold.
        drop_rows_with_missing(data_frame): Removes rows with missing values above the threshold.
    """

    def __init__(self, threshold=0.25):
        """
        Initializes the MissingDataHandler with the specified threshold.

        Parameters:
            threshold (float): Maximum ratio of missingness for dropping columns or rows.
        """
        self.threshold = threshold
        self.validate_threshold()

    def validate_threshold(self):
        """
        Validates the threshold attribute.
        """
        if not isinstance(self.threshold, (int, float)):
            raise TypeError("Threshold must be a numeric value")
        if not 0 <= self.threshold <= 1:
            raise ValueError("Threshold must be between 0 and 1")

    def detect_missing(self, data):
        """
        Detects missing values in a collection.

        Parameters:
            data (list, array, or Series): Collection containing data.

        Returns:
            Boolean array indicating missing (True) and non-missing data (False).
        """

        is_missing = np.isnan(data)
        return is_missing

    def count_missing(self, data):
        """
        Counts missing values in a collection.

        Parameters:
            data (list, array, or Series): Collection containing data.

        Returns:
            Number of missing values in collection
        """

        missing=self.detect_missing(data)
        n_missing=missing.sum()
        return n_missing

    def count_missing_in_dataframe(self, data_frame, axis=0):
        """
        Counts missing values in each row or column of a DataFrame.

        Parameters:
            data_frame (DataFrame): Pandas DataFrame containing only numeric values.
            axis (int, optional): Axis along which to count missing values.
                0 for columns, 1 for rows. Default is 0.

        Returns:
            Series: Pandas Series with the row/column index and the number of missing values.
        """
        validate_dataframe(data_frame)
        missing_values = data_frame.apply(self.detect_missing, axis=axis)
        n_missing_values = missing_values.sum(axis=axis)
        return n_missing_values

    def drop_columns_with_missing(self, data_frame):
        """
        Removes columns with missing values above the threshold.

        Parameters:
            data_frame (DataFrame): Pandas DataFrame containing only numeric values.

        Returns:
            DataFrame: DataFrame without columns with missingness higher than the threshold.
        """
        validate_dataframe(data_frame)
        missing = self.count_missing_in_dataframe(data_frame, axis=0)
        to_drop = missing[missing / len(data_frame) > self.threshold]
        data_frame = data_frame.drop(columns=to_drop.index)
        return data_frame

    def drop_rows_with_missing(self, data_frame):
        """
        Removes rows with missing values above the threshold.

        Parameters:
            data_frame (DataFrame): Pandas DataFrame containing only numeric values.

        Returns:
            DataFrame: DataFrame without rows with missingness higher than the threshold.
        """
        validate_dataframe(data_frame)
        missing = self.count_missing_in_dataframe(data_frame, axis=1)
        to_drop = missing[missing / len(data_frame.columns) > self.threshold]
        data_frame = data_frame.drop(index=to_drop.index)
        return data_frame