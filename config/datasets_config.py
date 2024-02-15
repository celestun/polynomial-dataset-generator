############### TARGET TYPES ##############
# The type of the independent variable Y.

# Indicates whether datasets with linear targets will be generated.
# Linear targets involve selecting a threshold in the original numerical values of Y.
# Values smaller than this threshold are set to 0, and values larger are set to 1.
GENERATE_LINEAR_TARGET = True

# Indicates whether datasets with non-linear targets will be generated.
# Non-linear targets involve selecting a boundary in the middle of all possible numerical values of Y.
# Values within this boundary are set to 1, while values outside the boundary are set to 0.
GENERATE_NON_LINEAR_TARGET = True

# Assert that at least one of GENERATE_LINEAR_TARGET or GENERATE_NON_LINEAR_TARGET is True
assert (
    GENERATE_LINEAR_TARGET or GENERATE_NON_LINEAR_TARGET
), "At least one of GENERATE_LINEAR_TARGET or GENERATE_NON_LINEAR_TARGET must be True"

############### CATEGORICAL ATTRIBUTES ##############
# For each of the following flags set to True, a corresponding dataset will be generated.
# Depending on the combination of flags, multiple datasets may be generated.
# For example, if all flags are True, a total of 8 datasets will be generated.

# Generates datasets with only numerical attributes.
GENERATE_ONLY_NUMBERS_DATASET = True

# Generates datasets with high-cardinality categorical attributes.
GENERATE_DATASET_WITH_HIGH_CARDINALITY_CAT_ATTRIBUTES = True

# Generates datasets with low-cardinality categorical attributes.
GENERATE_DATASET_WITH_LOW_CARDINALITY_CAT_ATTRIBUTES = True

# Generates datasets with binary categorical attributes.
GENERATE_DATASET_WITH_BINARY_CAT_ATTRIBUTES = True
