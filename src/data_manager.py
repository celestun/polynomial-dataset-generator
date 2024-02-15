import json
from datetime import datetime

import numpy as np
import pandas as pd

from config.logging import set_logger
from config.poly_params_config import NUMBER_OF_INSTANCES

logger = set_logger()


class DataManager:
    @classmethod
    def generate_independent_var_data(cls):
        """
        Generate independent variable data.

        This method generates random data for independent variables in a numpy array.

        Returns:
            np.ndarray: Array containing independent variable data.
        """
        rng = np.random.default_rng()
        return rng.random((NUMBER_OF_INSTANCES, 1))

    @classmethod
    def generate_binary_linear_target(cls, df):
        """
        Generate binary linear target variable based on the DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing numerical target data.

        Returns:
            pd.DataFrame: DataFrame with generated binary linear target variable.
        """
        df = df.copy()

        df["target"] = None
        half_index = len(df.index) // 2
        num_target = df["num_target"].tolist()
        num_target.sort(reverse=True)

        upper_half = num_target[:half_index]

        for index, row in df.iterrows():
            df.at[index, "target"] = row["num_target"] in upper_half

        cls._assert_data_balance(df)

        return df

    @classmethod
    def generate_binary_non_linear_target(cls, df):
        """
        Generate binary non-linear target variable based on the DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing numerical target data.

        Returns:
            pd.DataFrame: DataFrame with generated binary non-linear target variable.
        """
        df = df.copy()

        df["target"] = None
        quater_index_size = len(df.index) // 4
        num_target = df["num_target"].tolist()
        num_target.sort(reverse=True)

        upper_quater = num_target[:quater_index_size]
        lower_quater = num_target[-quater_index_size:]

        vals_to_be_true = upper_quater + lower_quater

        for index, row in df.iterrows():
            df.at[index, "target"] = row["num_target"] in vals_to_be_true

        cls._assert_data_balance(df)

        return df

    @classmethod
    def create_metadata(cls, vars, expression, cat_cols, name):
        """
        Create metadata dictionary for the dataset.

        Args:
            vars (list): List of variable names.
            expression (str): Polynomial expression used to generate the dataset.
            cat_cols (list): List of categorical variable names.
            name (str): Name of the dataset.

        Returns:
            dict: Metadata dictionary.
        """
        metadata = {
            "dataset_name": name,
            "desc": f"polynomial expression: {expression}",
            "dataset_source": None,
            "relative_path_to_dataset": f"./datasets/{name}/train_dataset.csv",
            "relative_path_to_unbalanced_dataset": None,
            "id_cols": [],
            "cat_cols": cat_cols,
            "time_cols": [],
            "num_cols": vars,
            "is_scaled": True,
            "cols_to_delete": [],
            "target": "target",
            "positive_values_are_represented_by": True,
        }

        return metadata

    @classmethod
    def save_dict_to_json(cls, dictionary, path_and_name):
        """
        Save dictionary to JSON file.

        Args:
            dictionary (dict): Dictionary to be saved.
            path_and_name (str): Path and name of the JSON file.
        """
        with open(path_and_name, "w") as write_file:
            json.dump(dictionary, write_file, indent=4)

    @classmethod
    def _assert_data_balance(cls, df):
        """
        Assert the balance of binary target variable distribution.

        Args:
            df (pd.DataFrame): DataFrame containing the binary target variable.
        """
        counts = df["target"].value_counts().tolist()

        positive_instances = (counts[1] / (counts[0] + counts[1])) * 100
        negative_instances = (counts[0] / (counts[0] + counts[1])) * 100

        assert positive_instances == negative_instances

    @classmethod
    def save_csv(cls, df, name_and_path):
        """
        Save DataFrame to CSV file.

        Args:
            df (pd.DataFrame): DataFrame to be saved.
            name_and_path (str): Path and name of the CSV file.
        """
        df.to_csv(name_and_path, index=False)

    @classmethod
    def load_json(cls, path_and_name):
        """
        Load JSON file into dictionary.

        Args:
            path_and_name (str): Path and name of the JSON file.

        Returns:
            dict: Loaded dictionary.
        """
        with open(path_and_name, "r") as read_file:
            return json.load(read_file)
