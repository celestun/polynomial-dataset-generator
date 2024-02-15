# Define an Enum for target types
from enum import Enum

from config import datasets_config
from config.cat_vars_config import (
    BINARY,
    INSTANCES_IN_HIGH_CARD_CAT_VAR,
    INSTANCES_IN_LOW_CARD_CAT_VAR,
    NO_CAT_INSTANCES,
)


class TargetType(Enum):
    LINEAR = "LINEAR"
    NON_LINEAR = "NON_LINEAR"


class CatAttributeType(Enum):
    NO_CATEGORICAL_ATTRIBUTES = "NO_CATEGORICAL_ATTRIBUTES"
    HIGH_CARDINALITY = "HIGH_CARDINALITY"
    LOW_CARDINALITY = "LOW_CARDINALITY"
    BINARY = "BINARY"


def get_datasets_properties():
    # Extract target types to generate
    target_types_to_generate = (
        [TargetType.LINEAR] if datasets_config.GENERATE_LINEAR_TARGET else []
    )
    target_types_to_generate.append(
        TargetType.NON_LINEAR
    ) if datasets_config.GENERATE_NON_LINEAR_TARGET else None

    # Extract categorical attribute properties
    cat_attributes_properties = [
        CatAttributeType.NO_CATEGORICAL_ATTRIBUTES
        if datasets_config.GENERATE_ONLY_NUMBERS_DATASET
        else None,
        CatAttributeType.HIGH_CARDINALITY
        if datasets_config.GENERATE_DATASET_WITH_HIGH_CARDINALITY_CAT_ATTRIBUTES
        else None,
        CatAttributeType.LOW_CARDINALITY
        if datasets_config.GENERATE_DATASET_WITH_LOW_CARDINALITY_CAT_ATTRIBUTES
        else None,
        CatAttributeType.BINARY
        if datasets_config.GENERATE_DATASET_WITH_BINARY_CAT_ATTRIBUTES
        else None,
    ]
    cat_attributes_properties = [prop for prop in cat_attributes_properties if prop]

    # Generate dataset configurations
    datasets_properties = []
    for target_type in target_types_to_generate:
        for categorical_properties in cat_attributes_properties:
            dataset_config = {
                "target_type": target_type.value,
                "cat_attributes_properties": categorical_properties.value,
            }
            datasets_properties.append(dataset_config)

    return datasets_properties


def map_cat_attributes(properties):
    # Define the mapping dictionary
    mapping = {
        CatAttributeType.NO_CATEGORICAL_ATTRIBUTES.value: NO_CAT_INSTANCES,
        CatAttributeType.HIGH_CARDINALITY.value: INSTANCES_IN_HIGH_CARD_CAT_VAR,
        CatAttributeType.LOW_CARDINALITY.value: INSTANCES_IN_LOW_CARD_CAT_VAR,
        CatAttributeType.BINARY.value: BINARY,
    }

    # Map the value using the dictionary
    cat_attributes_property = mapping.get(properties["cat_attributes_properties"])

    return cat_attributes_property
