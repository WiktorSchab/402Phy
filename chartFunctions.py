import matplotlib.pyplot as plt

def plot_lnP_lnT(lnT_list, lnP_list):
    """
    Plots the relationship between ln(P) and ln(T) using matplotlib.

    Parameters:
    lnT_list (list): List of natural logarithms of temperatures.
    lnP_list (list): List of natural logarithms of power.
    """
    plt.figure(figsize=(8, 6))
    plt.plot(lnT_list, lnP_list, color='red', label='Line connecting points')
    plt.scatter(lnT_list, lnP_list, color='red', label='Data points')
    plt.xlabel('ln(T)', fontsize=12)
    plt.ylabel('ln(P)', fontsize=12)
    plt.title('Plot of ln(P) vs ln(T)', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.show()


def generate_table(data, lnT_list, lnP_list):
    """
    Generates a table displaying the measured and calculated values.

    Parameters:
    data (list): A list of dictionaries containing measurement data and calculated values.
    lnT_list (list): List of natural logarithms of temperatures.
    lnP_list (list): List of natural logarithms of power.
    """
    headers = ["Lp.", "U [V]", "I [A]", "P [W]", "t1 [°C]", "t1śr [°C]", "T [K]", "ln(T)", "ln(P)"]
    table_data = []

    for i, record in enumerate(data, start=1):
        row = [
            i,
            round(record["U"], 2),
            round(record["I"], 2),
            round(record["P"], 2),
            ", ".join(map(str, record["t1"])),
            round(record["t1sr"], 2),
            round(record["T"], 2),
            round(lnT_list[i - 1], 2),
            round(lnP_list[i - 1], 2),
        ]
        table_data.append(row)

    # Create the table using Matplotlib
    fig, ax = plt.subplots(figsize=(16, 8))  # Increase figure size
    ax.axis("tight")
    ax.axis("off")
    table = ax.table(cellText=table_data, colLabels=headers, cellLoc="center", loc="center")

    # Automatically adjust font size and column width to fit the cells
    table.auto_set_font_size(False)
    table.set_fontsize(12)  # Adjust font size to fit better

    # Auto set column width
    table.auto_set_column_width(col=list(range(len(headers))))

    # Increase cell height and width based on figure size (overall)
    table.scale(2, 2)  # Scale the table to increase the cell size automatically

    plt.title("Tabela wyników pomiarów", fontsize=18, pad=30)  # Adjusted title size and padding
    plt.show()
