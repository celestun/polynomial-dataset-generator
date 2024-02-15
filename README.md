# Synthetic Dataset Generator

This project is a synthetic dataset generator designed to create datasets with polynomial expressions and categorical attributes. It offers flexibility in configuring the types of datasets to generate, including linear and non-linear target variables, as well as various types of categorical attributes.

## Getting Started

To get started with using the synthetic dataset generator, follow these steps:

1. Clone the repository to your local machine.

2. Install the required dependencies. You can use `pip` to install the dependencies listed in the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

The project consists of the following main components:

- `config`: Contains configuration files for defining dataset parameters, logging settings, and categorical variable properties.
- `datasets`: Stores the generated datasets and their corresponding metadata files.
- `src`: Contains the source code for the dataset generator, including modules for generating polynomial expressions, managing categorical attributes, and saving/loading datasets.

## Configuration

You can configure the synthetic dataset generator by modifying the configuration files located in the `config` directory:

- `base.py`: Defines base configurations such as file paths and the number of datasets to generate.
- `cat_vars_config.py`: Configures the properties of categorical variables, including the percentage of categorical variables, cardinality, and instances per category.
- `datasets_config.py`: Specifies the types of datasets to generate, including linear and non-linear target variables, and the presence of categorical attributes.
- `poly_params_config.py`: Sets parameters for generating polynomial expressions, such as the number of variables, degrees, and coefficients.
- `logging.py`: Configures logging settings for the project.

## Generating Datasets

To generate synthetic datasets, run the `entrypoint.py` script located at the project root. This script iterates through the specified number of datasets to generate and calls the `main_routine.py` module to perform dataset generation.

```bash
python entrypoint.py
```

The generated datasets will be saved in the `datasets` directory, along with corresponding metadata files containing information about the datasets.

## Dataset Configuration Service

The `dataset_configuration_service.py` module provides functions for defining dataset properties, including target types and categorical attribute properties. This module facilitates the generation of dataset configurations based on the settings specified in the configuration files.

## Contributing

Contributions to the synthetic dataset generator project are welcome! If you have any ideas for improvements or new features, feel free to open an issue or submit a pull request.
