import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import dill
import os
from src.utils import create_directory


class EffectsHandler:
    """
    Class for fitting linear models to the data and obtaining residuals

    The class takes a data manager as input, and fits a linear model using the
    formula specified in the constructor for each metabolite. The residuals
    are then extracted from the fitted models and returned as a pandas DataFrame.

    If a path to a directory is provided, the fitted models will be saved as
    pickle files in that directory.

    Attributes:
        data_manager (DataManager): DataManager instance containing the data
        formula (str): formula used to fit the linear model
        merged (DataFrame): merged dataframe of sample metadata and data
        residuals (DataFrame): dataframe of residuals, initially full of NaNs
    """

    def __init__(
        self, data_manager, formula="C(slaughter) + C(batch) + weight", models_path=None
    ) -> None:
        """
        Initialize the class.

        Parameters:
            data_manager (DataManager): DataManager instance containing the data
            formula (str): formula used to fit the linear model
            models_path (str): path to directory where models will be saved
        """
        self.data_manager = data_manager
        self.formula = formula
        self.merged = self.data_manager.merge_sample_metadata_data()
        self.residuals = self.data_manager.data.copy()
        self.residuals.loc[:] = np.nan

    def fit_model(self, metabolite):
        """
        Fit a linear model using the formula specified in the constructor.

        Parameters:
            metabolite (str): name of metabolite to fit model for

        Returns:
            residuals (Series): residuals from the fitted model
            model (RegressionResults): fitted model
        """
        model = smf.ols(f"Q('{metabolite}') ~ {self.formula}", self.merged)
        fitted_model = model.fit()
        residuals = fitted_model.resid
        return residuals, model

    def get_all_residuals(self, models_path=None):
        """
        Fit a linear model for each metabolite and extract residuals.

        Parameters:
            models_path (str): path to directory where models will be saved

        Returns:
            residuals (DataFrame): dataframe of residuals for all metabolites
        """
        if models_path:
            create_directory(models_path)
        for metabolite in self.data_manager.metabolites:
            residuals, model = self.fit_model(metabolite)
            self.residuals[metabolite] = residuals
            if models_path:
                with open(f"{models_path}/{metabolite}.pickle", "wb") as handle:
                    dill.dump(model, handle)
        return self.residuals
