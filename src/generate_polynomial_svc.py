import random

from config.logging import set_logger

logger = set_logger()


class GeneratePolynomialSvc:
    @classmethod
    def define_params(
        cls,
        min_num_of_vars,
        max_num_of_vars,
        max_num_of_terms,
        min_coef_value,
        max_coef_value,
    ):
        """
        Define parameters for generating a polynomial.

        Args:
            min_num_of_vars (int): Minimum number of variables.
            max_num_of_vars (int): Maximum number of variables.
            max_num_of_terms (int): Maximum number of terms in the polynomial.
            min_coef_value (float): Minimum value for the coefficients.
            max_coef_value (float): Maximum value for the coefficients.

        Returns:
            tuple: A tuple containing the number of variables, number of terms, and coefficients.
        """
        # Select a random number of variables.
        num_of_vars = random.randint(min_num_of_vars, max_num_of_vars)
        # Select a random number of terms.
        num_of_terms = random.randint(1, max_num_of_terms)

        # Generate coefficients for each term.
        coefficients = {}
        for term in range(num_of_terms):
            coefficients["c_term_" + str((term + 1))] = random.uniform(
                min_coef_value, max_coef_value
            )

        logger.debug(f"Number of variables: {num_of_vars}")
        logger.debug(f"Number of terms: {num_of_terms}")
        logger.debug(f"Coefficients: {coefficients}")

        return num_of_vars, num_of_terms, coefficients

    @classmethod
    def create_string_expression(
        cls, num_of_vars, min_degree, max_degree, num_of_terms, coefficients
    ):
        """
        Create a string expression for the polynomial.

        Args:
            num_of_vars (int): Number of variables.
            min_degree (int): Minimum degree for variables.
            max_degree (int): Maximum degree for variables.
            num_of_terms (int): Number of terms in the polynomial.
            coefficients (dict): Coefficients for each term.

        Returns:
            tuple: A tuple containing the polynomial expression and variables used.
        """
        variables = cls._get_vars(num_of_vars)

        # Create terms for the polynomial.
        terms = {}
        for term in range(num_of_terms):
            term_name = "term_" + str(term + 1)
            vars_with_exp = []
            for var in variables:
                # Select exponent for each variable.
                var_exponent = random.randint(min_degree, max_degree)
                vars_with_exp.append(f"({var}**{var_exponent})")
            # Join variables with their exponents.
            term_expression = " * ".join(vars_with_exp)
            # Multiply the term by its coefficient.
            term_expression = f"{coefficients['c_' + term_name]} * {term_expression}"
            terms[term_name] = term_expression

        # Join terms to create the polynomial expression.
        polynomial_expression = " + ".join(terms.values())

        return polynomial_expression, variables

    @classmethod
    def _get_vars(cls, num_of_vars):
        """
        Generate variable names based on the number of variables.

        Args:
            num_of_vars (int): Number of variables.

        Returns:
            list: A list containing variable names.
        """
        return [f"v{i}" for i in range(1, num_of_vars + 1)]
