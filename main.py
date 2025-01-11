from calcFunctions import calc_power, temp_average, temp_average_kelvin, natural_log_temp, natural_log_power, calc_temp, \
    x_factor, y_factor, measurement_error

from chartFunctions import plot_lnP_lnT, generate_table


def main():
    # Sample data
    sample_data = [
        {"U": 3.3, "I": 2.2, "t1": [940.0, 920.0, 930.0, 940.0, 935.0]},
        {"U": 4.2, "I": 2.5, "t1": [1060.0, 1045.0, 1042.0, 1025.0, 980.0]},
        {"U": 5.58, "I": 2.90, "t1": [1158.0, 1120.0, 1122.0, 1140.0, 1142.0]},
        {"U": 6.76, "I": 3.20, "t1": [1208.0, 1220.0, 1270.0, 1225.0, 1258.0]},
        {"U": 8.02, "I": 4.38, "t1": [1308.0, 1310.0, 1390.0, 1350.0, 1342.0]},
    ]

    sample_data2 = [
        {"U": 3.18, "I": 2.16, "t1": [1220.0, 1220.0, 1240.0, 1220.0, 1240.0]},
        {"U": 4.23, "I": 2.5, "t1": [1360.0, 1320.0, 1340.0, 1340.0, 1340.0]},
        {"U": 4.91, "I": 2.70, "t1": [1400.0, 1400.0, 1400.0, 1420.0, 1400.0]},
        {"U": 5.76, "I": 2.90, "t1": [1500.0, 1500.0, 1520.0, 1520.0, 1500.0]},
        {"U": 6.39, "I": 3.10, "t1": [1580.0, 1550.0, 1600.0, 1590.0, 1580.0]},
    ]

    data_in_use = sample_data.copy()

    calc_power(data_in_use)
    temp_average(data_in_use)
    temp_average_kelvin(data_in_use)

    # Lists of natural logs
    lnT_list = natural_log_temp(data_in_use)
    lnP_list = natural_log_power(data_in_use)

    # Calculating average temp and temp
    Tsr = sum(record["t1sr"] for record in data_in_use) / len(data_in_use) + 273.15
    T = calc_temp(Tsr)

    # Calculating average x and y
    x_av = sum(lnT_list) / len(lnT_list)
    y_av = sum(lnP_list) / len(lnP_list)

    # Calculating x and y factors
    Sxx = x_factor(lnT_list, x_av)
    Sxy = y_factor(lnT_list, lnP_list, x_av, y_av)

    # Calculating temperature power exponent
    a = Sxy/Sxx

    # Calculates the residual standard error
    a_e = measurement_error(y_av, x_av, a, lnT_list, lnP_list)

    # Displaying results
    print(f"Wartość wykładnika wynosi {round(a,2)}±{round(a_e,2)}")
    plot_lnP_lnT(lnT_list, lnP_list)
    generate_table(data_in_use, lnT_list, lnP_list)


if __name__ == '__main__':
    main()
