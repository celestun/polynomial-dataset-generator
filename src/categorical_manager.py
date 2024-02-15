from config.logging import set_logger

logger = set_logger()
import math

from config.cat_vars_config import PERC_OF_CAT_VARS


class CategoricalManager:
    @classmethod
    def create_cat_vars(cls, df, vars, cardinality_number):
        """
        Convert selected numeric variables into categorical variables in the DataFrame.

        Args:
            df (pd.DataFrame): Input DataFrame.
            vars (list): List of variables to consider for conversion.
            cardinality_number (int): Desired cardinality of the categorical variables.

        Returns:
            tuple: A tuple containing the modified DataFrame and a list of created categorical variables.
        """
        if cardinality_number == 0:
            return df, []

        high_card_df = df.copy()
        num_of_numeric_vars = len(vars)
        float_expected_cat_instances = num_of_numeric_vars * PERC_OF_CAT_VARS

        # Calculate the expected number of categorical instances
        expected_cat_instances = max(1, math.floor(float_expected_cat_instances))

        # Select variables to convert
        cat_vars = vars[:expected_cat_instances]

        for cat_var in cat_vars:
            # Sort values of the selected variable
            num_values_to_convert = high_card_df[cat_var].tolist()
            num_values_to_convert.sort(reverse=True)

            # Determine the number of instances in each category
            total_num_instance_in_each_cat = int(
                len(num_values_to_convert) / cardinality_number
            )

            num_to_cat_map = {}
            counter_group = 1
            counter_iter = 0

            # Map numeric values to categorical labels
            for num_instance in num_values_to_convert:
                counter_iter += 1
                num_to_cat_map[str(num_instance)] = f"cat_inst_{counter_group}"
                if counter_iter == total_num_instance_in_each_cat:
                    counter_iter = 0
                    counter_group += 1

            # Convert numeric values to categorical labels
            for index, row in high_card_df.iterrows():
                high_card_df.at[index, cat_var] = num_to_cat_map[str(row[cat_var])]

        return high_card_df, cat_vars
