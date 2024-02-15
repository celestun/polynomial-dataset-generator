import os
from datetime import datetime

import pandas as pd

from config.base import (
    BASE_NAME,
    PATH_TO_METADATA_FILES,
    PATH_TO_STORE_GENERATED_DATASETS,
)
from config.cat_vars_config import (
    BINARY,
    INSTANCES_IN_HIGH_CARD_CAT_VAR,
    INSTANCES_IN_LOW_CARD_CAT_VAR,
    NO_CAT_INSTANCES,
)
from config.datasets_config import GENERATE_LINEAR_TARGET, GENERATE_NON_LINEAR_TARGET
from config.logging import set_logger
from config.poly_params_config import params as pol_params
from src.categorical_manager import CategoricalManager
from src.data_manager import DataManager
from src.generate_polynomial_svc import GeneratePolynomialSvc
from src.services.dataset_configuration_service import (  # Import the function
    CatAttributeType,
    TargetType,
    get_datasets_properties,
    map_cat_attributes,
)

logger = set_logger()


def start():
    """
    Generates synthetic datasets based on specified parameters, including polynomial expressions and categorical attributes.

    Steps:
        1. Load main configuration file.
        2. Generate an execution ID based on the current date and time.
        3. Define polynomial parameters and create a polynomial expression string.
        4. Generate random values for independent variables and evaluate the polynomial expression.
        5. Create a dataset with numerical and categorical variables.
        6. Optionally generate linear and non-linear target variables.
        7. Iterate through dataset properties and generate datasets according to specified properties:
            a. Map categorical attribute properties.
            b. Create categorical variables based on the mapped properties.
            c. Build dataset name and path.
            d. Save generated dataset and metadata files.
    """

    path_to_gen_datasets = PATH_TO_STORE_GENERATED_DATASETS

    # use date as identifier of the set of generated datasets
    exec_id = datetime.today().strftime("%Y%m%d%H%M%S")
    logger.info("Generating synthetic dataset")
    logger.info(pol_params)

    num_of_vars, num_of_terms, coeficients = GeneratePolynomialSvc.define_params(
        pol_params["min_num_of_vars"],
        pol_params["max_num_of_vars"],
        pol_params["max_num_of_terms"],
        pol_params["min_coef_value"],
        pol_params["max_coef_value"],
    )

    string_expression, vars = GeneratePolynomialSvc.create_string_expression(
        num_of_vars,
        pol_params["min_degree"],
        pol_params["max_degree"],
        num_of_terms,
        coeficients,
    )

    logger.info(f"string_expression: {string_expression}")

    dict_to_convert_to_dataframe = {}

    # generate random numbers in a determined range for independnt vars V1, V2, ... Vn.
    # store those vars as global.
    for num in range(num_of_vars):
        globals()["v" + str(num + 1)] = DataManager.generate_independent_var_data()
        dict_to_convert_to_dataframe["v" + str(num + 1)] = globals()[
            "v" + str(num + 1)
        ].flatten()

    # evaluate string polynomial
    final_result = eval(string_expression)

    ## add numerical dependent variable
    dict_to_convert_to_dataframe["num_target"] = final_result.flatten()

    ################ create targets
    df = pd.DataFrame(dict_to_convert_to_dataframe)

    datasets_properties = get_datasets_properties()

    if GENERATE_LINEAR_TARGET:
        df_linear_target = DataManager.generate_binary_linear_target(df)
        del df_linear_target["num_target"]

    if GENERATE_NON_LINEAR_TARGET:
        df_non_linear_target = DataManager.generate_binary_non_linear_target(df)
        del df_non_linear_target["num_target"]

    for properties in datasets_properties:
        base_dataset = (
            df_linear_target
            if properties["target_type"] == TargetType.LINEAR
            else df_non_linear_target
        )

        # Map the categorical attribute properties
        cat_attributes_property = map_cat_attributes(properties)

        # if cat_attributes_property:
        (
            dataset_to_store,
            cat_vars,
        ) = CategoricalManager.create_cat_vars(
            base_dataset, vars, cat_attributes_property
        )
        num_vars = vars.copy()
        for cat_var in cat_vars:
            num_vars.remove(cat_var)

        # build dataset name and path
        target_type_name = properties["target_type"].lower()
        cat_attributes_name = properties["cat_attributes_properties"].lower()
        main_name = f"{BASE_NAME}_{exec_id}_{target_type_name}_{cat_attributes_name}"
        name_and_path = os.path.join(path_to_gen_datasets, f"{main_name}.csv")
        # store dataset and metadata
        DataManager.save_csv(dataset_to_store, name_and_path)

        # Store dataset
        metadata = DataManager.create_metadata(
            num_vars, string_expression, cat_vars, main_name
        )
        # Store metadata
        metadata_file_path_and_name = os.path.join(
            PATH_TO_METADATA_FILES, f'{metadata["dataset_name"]}.json'
        )
        DataManager.save_dict_to_json(metadata, metadata_file_path_and_name)
