import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import numpy as np

def plot_barplot(data: pd.DataFrame, x_axis: pd.Series, y_axis: pd.Series, sem_values: pd.Series, x_axis_2: pd.Series, individual_points: pd.Series, y_label: str, save_path:str):
    """Create a barplot with error bars and individual points, and save it as a file

    Args:
        data (pd.DataFrame): data frame of the data for the graph
        x_axis (pd.Series): groups for the x axis for the bars
        y_axis (pd.Series): length of the y axis (mean)
        sem_values (pd.Series): sem of the y axis for error bars
        x_axis_2 (pd.Series): groups of the x axis for the individual points
        individual_points (pd.Series): individual values
        y_label (str): name for the y axis
        save_path (str): path to the directory to save the files
    """    
    fig, ax = plt.subplots()
    ax = sns.barplot(x = x_axis, y = y_axis, data = data, palette = "Blues", errorbar = None)
    # Manually adding error bars:
    for i, sem in enumerate(sem_values):
        ax.errorbar(i, y_axis.iloc[i], yerr = sem, fmt = "none", capsize = 5, color = "black")
    # Add indiviual data points
    for i, category in enumerate(x_axis.unique()): # Assuming x_axis is a column in data with unique categories
        y_values = individual_points[x_axis_2 == category]
        x_values = np.random.normal(loc = i, scale = 0.1, size = (len(y_values))) # random jitter (0.1) for all individual points (not spread on a straight line)
        ax.scatter(x_values, y_values, color = "black")
    # Set title and x and y axis labels
    ax.set_xlabel("Genotype")
    ax.set_ylabel(y_label)
    # Show and save the plot
    plt.show()
    print("saving graph...")
    fig.savefig(save_path, dpi=300)