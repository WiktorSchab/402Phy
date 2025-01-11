from math import log, sqrt


def calc_power(data):
    """
    Calculates power (P = U * I) for each record and adds it as a new key "P".

    Parameters:
    data (list): A list of dictionaries where each dictionary contains 'U' (voltage) and 'I' (current).
    """
    for record in data:
        # Calculate power (P = U * I) and add it to the record
        record["P"] = record["U"] * record["I"]


def temp_average(data):
    """
    Calculates the average temperature from the 't1' list for each record and adds it as a new key 't1sr'.

    Parameters:
    data (list): A list of dictionaries where each dictionary contains a list of temperatures under the key 't1'.
    """
    for record in data:
        # Calculate the sum of temperatures (average can be added if needed)
        record["t1sr"] = sum(record["t1"]) / 5


def temp_average_kelvin(data):
    """
    Converts the average temperature to Kelvin by adding 273.15 and stores it under the key 'T'.

    Parameters:
    data (list): A list of dictionaries where each dictionary contains the average temperature in 't1sr'.
    """
    for record in data:
        # Convert temperature from Celsius to Kelvin
        record["T"] = record["t1sr"] + 273.15


def natural_log_temp(data):
    """
    Computes the natural logarithm of temperatures in Kelvin for each record.

    Parameters:
    data (list): A list of dictionaries where each dictionary contains temperature in Kelvin under the key 'T'.

    Returns:
    list: A list of natural logarithms of temperatures.
    """
    lnT_list = []
    for record in data:
        lnT_list.append(log(record["T"]))
    return lnT_list


def natural_log_power(data):
    """
    Computes the natural logarithm of power for each record.

    Parameters:
    data (list): A list of dictionaries where each dictionary contains power under the key 'P'.

    Returns:
    list: A list of natural logarithms of power.
    """
    lnP_list = []
    for record in data:
        lnP_list.append(log(record["P"]))
    return lnP_list


def calc_temp(Tsr):
    """
    Calculates the corrected temperature using the formula based on Planck's law.

    Parameters:
    Tsr (float): The average luminance temperature in Kelvin.

    Returns:
    float: The corrected temperature in Kelvin.
    """
    # constant: 650nm = 650e-9
    lambda_value = 650e-9
    # constant: 0.01338m*K
    constant = 0.01338
    lna = log(0.45)

    T = 1 / (1 / Tsr + (lambda_value / constant) * lna)
    return T


def x_factor(lnT_list, x_av):
    """
    Calculates the variance component Sxx for regression analysis.

    Parameters:
    lnT_list (list): List of natural logarithms of temperatures.
    x_av (float): Average of the natural logarithms of temperatures.

    Returns:
    float: The Sxx value for regression analysis.
    """
    sum_x = 0
    for x in lnT_list:
        sum_x += pow((x-x_av), 2)
    return sum_x


def y_factor(lnT_list, lnP_list, x_av, y_av):
    """
    Calculates the covariance component Sxy for regression analysis.

    Parameters:
    lnT_list (list): List of natural logarithms of temperatures.
    lnP_list (list): List of natural logarithms of power.
    x_av (float): Average of the natural logarithms of temperatures.
    y_av (float): Average of the natural logarithms of power.

    Returns:
    float: The Sxy value for regression analysis.
    """
    sum_y = 0
    for i in range(0, len(lnT_list)):
        sum_y += (lnT_list[i] - x_av) * (lnP_list[i] - y_av)
    return sum_y


def measurement_error(y_av, x_av, a, lnT_list, lnP_list):
    """
    Calculates the residual standard error for the regression model.

    Parameters:
    y_av (float): Average of the natural logarithms of power.
    x_av (float): Average of the natural logarithms of temperatures.
    a (float): Slope of the regression line.
    lnT_list (list): List of natural logarithms of temperatures.
    lnP_list (list): List of natural logarithms of power.

    Returns:
    float: The residual standard error.
    """
    # Calculate the intercept of the regression line
    b = y_av - a * x_av

    # Compute the sum of squared residuals
    sumY = 0
    for i in range(0, len(lnT_list)):
        expected_y = a * lnT_list[i] + b  # Corrected regression equation
        sumY += (lnP_list[i] - expected_y) ** 2

    # Degrees of freedom: number of data points minus 2 (for slope and intercept)
    degrees_of_freedom = len(lnT_list) - 2

    # Calculate the residual standard error
    residual_standard_error = sqrt(sumY / degrees_of_freedom)
    return residual_standard_error